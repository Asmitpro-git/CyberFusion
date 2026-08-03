from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.exceptions import (
    DuplicateEmailError,
    DuplicateUsernameError,
    InactiveAccountError,
    InvalidRefreshTokenError,
    LockedAccountError,
    WeakPasswordError,
    WrongPasswordError,
)
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import TokenData, create_access_token, create_refresh_token, decode_token, verify_token
from app.config.settings import get_settings
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, AuthTokenResponse, UserSummary


@dataclass(frozen=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str


def _utc_now() -> datetime:
    return datetime.now(UTC)


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()
        self.users = UserRepository(session)
        self.roles = RoleRepository(session)

    def _commit(self) -> None:
        self.session.commit()

    def _rollback(self) -> None:
        self.session.rollback()

    def _password_policy_violations(self, password: str) -> list[str]:
        violations: list[str] = []
        if len(password) < self.settings.auth_password_min_length:
            violations.append(f"must be at least {self.settings.auth_password_min_length} characters long")
        if self.settings.auth_password_require_uppercase and not re.search(r"[A-Z]", password):
            violations.append("must include at least one uppercase letter")
        if self.settings.auth_password_require_lowercase and not re.search(r"[a-z]", password):
            violations.append("must include at least one lowercase letter")
        if self.settings.auth_password_require_digit and not re.search(r"\d", password):
            violations.append("must include at least one digit")
        if self.settings.auth_password_require_special and not re.search(r"[^A-Za-z0-9]", password):
            violations.append("must include at least one special character")
        return violations

    def _validate_password_strength(self, password: str) -> None:
        violations = self._password_policy_violations(password)
        if violations:
            raise WeakPasswordError("Password must " + ", ".join(violations))

    def _build_user_summary(self, user: User) -> UserSummary:
        role = user.role
        if role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User role is not available")
        return UserSummary.model_validate(user)

    def _issue_tokens(self, user: User) -> TokenPair:
        role = user.role
        if role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User role is not available")
        permissions = dict(role.permissions)
        return TokenPair(
            access_token=create_access_token(
                user_id=user.id,
                username=user.username,
                role=role.name,
                permissions=permissions,
            ),
            refresh_token=create_refresh_token(
                user_id=user.id,
                username=user.username,
                role=role.name,
                permissions=permissions,
            ),
        )

    def _auth_response(self, user: User) -> AuthResponse:
        tokens = self._issue_tokens(user)
        return AuthResponse(
            tokens=AuthTokenResponse(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
                expires_in_minutes=self.settings.jwt_access_token_expire_minutes,
            ),
            user=self._build_user_summary(user),
        )

    def _get_role_for_registration(self, role_name: str | None) -> Role:
        requested_role_name = (role_name or "Viewer").strip()
        role = self.roles.get_by_name(requested_role_name)
        if role is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requested role does not exist")
        return role

    def register(self, *, username: str, email: str, password: str, role_name: str | None = None) -> AuthResponse:
        normalized_username = username.strip()
        normalized_email = email.strip().lower()
        if self.users.get_by_username(normalized_username) is not None:
            raise DuplicateUsernameError()
        if self.users.get_by_email(normalized_email) is not None:
            raise DuplicateEmailError()

        self._validate_password_strength(password)
        role = self._get_role_for_registration(role_name)

        try:
            user = self.users.create(
                username=normalized_username,
                email=normalized_email,
                hashed_password=hash_password(password),
                role_id=role.id,
                is_active=True,
                is_verified=False,
            )
            user.role = role
            user.last_login = _utc_now()
            self._commit()
            return self._auth_response(user)
        except Exception:
            self._rollback()
            raise

    def _lock_account(self, user: User) -> None:
        user.failed_login_attempts = self.settings.auth_max_failed_login_attempts
        user.locked_until = _utc_now() + timedelta(minutes=self.settings.auth_lockout_minutes)

    def _mark_failed_login(self, user: User) -> None:
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= self.settings.auth_max_failed_login_attempts:
            self._lock_account(user)

    def login(self, *, username_or_email: str, password: str) -> AuthResponse:
        identifier = username_or_email.strip()
        user = self.users.get_by_username_or_email(identifier)
        if user is None:
            raise WrongPasswordError()

        if not user.is_active:
            raise InactiveAccountError()

        if user.locked_until is not None and user.locked_until > _utc_now():
            raise LockedAccountError()

        if not verify_password(password, user.hashed_password):
            try:
                self._mark_failed_login(user)
                self._commit()
            except Exception:
                self._rollback()
                raise
            raise WrongPasswordError()

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = _utc_now()
        if user.role is None:
            loaded_user = self.users.get_with_role_by_id(user.id)
            if loaded_user is not None:
                user = loaded_user
        try:
            self._commit()
            return self._auth_response(user)
        except Exception:
            self._rollback()
            raise

    def refresh(self, *, refresh_token: str) -> AuthResponse:
        token_data = verify_token(refresh_token, expected_type="refresh")
        return self._auth_response(self._load_active_user_from_token(token_data))

    def logout(self, *, refresh_token: str | None = None) -> None:
        if refresh_token:
            try:
                verify_token(refresh_token, expected_type="refresh")
            except HTTPException as exc:
                raise InvalidRefreshTokenError() from exc

    def current_user(self, *, user_id: UUID) -> UserSummary:
        user = self.users.get_with_role_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise InactiveAccountError()
        if user.role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User role is not available")
        return self._build_user_summary(user)

    def change_password(self, *, user_id: UUID, current_password: str, new_password: str) -> AuthResponse:
        user = self.users.get_with_role_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise InactiveAccountError()
        if not verify_password(current_password, user.hashed_password):
            raise WrongPasswordError()

        self._validate_password_strength(new_password)
        if verify_password(new_password, user.hashed_password):
            raise WeakPasswordError("New password must be different from the current password")

        user.hashed_password = hash_password(new_password)
        user.last_login = _utc_now()
        user.failed_login_attempts = 0
        user.locked_until = None
        try:
            self._commit()
            return self._auth_response(user)
        except Exception:
            self._rollback()
            raise

    def _load_active_user_from_token(self, token_data: TokenData) -> User:
        try:
            user_id = UUID(token_data["user_id"])
        except ValueError as exc:
            raise InvalidRefreshTokenError() from exc

        user = self.users.get_with_role_by_id(user_id)
        if user is None:
            raise InvalidRefreshTokenError()
        if not user.is_active:
            raise InactiveAccountError()
        if user.role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User role is not available")
        return user