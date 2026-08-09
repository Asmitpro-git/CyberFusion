from __future__ import annotations

from dataclasses import dataclass
from urllib import request
from urllib import request
from uuid import UUID

from fastapi import HTTPException, Request, status
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match
from fastapi.responses import JSONResponse

from app.auth.dependencies import AuthenticatedUser
from app.auth.jwt import verify_token
from app.database.session import SessionLocal
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.rbac.decorators import PERMISSION_ATTRIBUTE, ROLE_ATTRIBUTE
from app.rbac.engine import PermissionEngine, RoleEngine


@dataclass(frozen=True, slots=True)
class AuthorizationContext:
    user: AuthenticatedUser
    token_type: str


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        route = self._match_route(request)

        if route is None:
            return await call_next(request)

        required_roles = tuple(
            getattr(route.endpoint, ROLE_ATTRIBUTE, ())
        )

        required_permissions = tuple(
            getattr(route.endpoint, PERMISSION_ATTRIBUTE, ())
        )

        if not required_roles and not required_permissions:
            return await call_next(request)

        try:
            context = self._resolve_authorization_context(request)

            self._enforce_requirements(
                context.user,
                required_roles,
                required_permissions,
            )

            request.state.authenticated_user = context.user
            request.state.authorization_context = context

            return await call_next(request)

        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": exc.detail,
                },
            )

    def _match_route(self, request: Request) -> APIRoute | None:
        for route in request.app.routes:
            if not isinstance(route, APIRoute):
                continue
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                return route
        return None

    def _resolve_authorization_context(self, request: Request) -> AuthorizationContext:
        token = self._extract_bearer_token(request)
        token_data = verify_token(token, expected_type="access")
        user = self._load_user(token_data["user_id"])
        role = user.role
        if role is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role is not assigned")

        authenticated_user = AuthenticatedUser(
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
        return AuthorizationContext(user=authenticated_user, token_type=token_data["token_type"])

    def _extract_bearer_token(self, request: Request) -> str:
        authorization_header = request.headers.get("Authorization", "")
        prefix = "Bearer "
        if not authorization_header.startswith(prefix):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        token = authorization_header[len(prefix) :].strip()
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return token

    def _load_user(self, user_id: str) -> User:
        try:
            user_uuid = UUID(user_id)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized") from exc

        with SessionLocal() as session:
            repository = UserRepository(session)
            user = repository.get_with_role_by_id(user_uuid)
            if user is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
            if not user.is_active:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
            return user

    def _enforce_requirements(
        self,
        user: AuthenticatedUser,
        required_roles: tuple[str, ...],
        required_permissions: tuple[str, ...],
    ) -> None:
        if required_roles and not RoleEngine.has_any_role(user.role.name, required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role privileges")
        if required_permissions and not PermissionEngine.has_permissions(user.permissions, required_permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permission privileges")