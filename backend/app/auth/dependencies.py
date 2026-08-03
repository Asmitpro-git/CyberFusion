from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.jwt import TokenData, verify_token
from app.core.dependencies import get_database_session
from app.models.role import Role
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    id: UUID
    username: str
    email: str
    role: Role
    permissions: dict[str, Any]
    is_active: bool
    is_verified: bool
    failed_login_attempts: int
    locked_until: Any
    last_login: Any
    created_at: Any
    updated_at: Any


def _get_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return credentials.credentials


def _build_authenticated_user(user: User, role: Role) -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user.id,
        username=user.username,
        email=user.email,
        role=role,
        permissions=dict(role.permissions),
        is_active=user.is_active,
        is_verified=user.is_verified,
        failed_login_attempts=user.failed_login_attempts,
        locked_until=user.locked_until,
        last_login=user.last_login,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_database_session)],
) -> AuthenticatedUser:
    cached_user = getattr(request.state, "authenticated_user", None)
    if isinstance(cached_user, AuthenticatedUser):
        return cached_user

    token = _get_token(credentials)
    token_data: TokenData = verify_token(token, expected_type="access")

    try:
        user_id = UUID(token_data["user_id"])
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    user_repository = UserRepository(session)
    user = user_repository.get_with_role_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    role = user.role
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not assigned",
        )

    return _build_authenticated_user(user, role)


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]