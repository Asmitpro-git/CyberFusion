from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.core.dependencies import DatabaseSession
from app.schemas.auth import (
    AuthResponse,
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    RefreshTokenRequest,
    RegisterRequest,
    UserSummary,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(session=DatabaseSession) -> AuthService:
    return AuthService(session)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, session=DatabaseSession) -> AuthResponse:
    service = AuthService(session)
    return service.register(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        role_name=payload.role_name,
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, session=DatabaseSession) -> AuthResponse:
    service = AuthService(session)
    return service.login(username_or_email=payload.username_or_email, password=payload.password)


@router.post("/refresh", response_model=AuthResponse)
def refresh(payload: RefreshTokenRequest, session=DatabaseSession) -> AuthResponse:
    service = AuthService(session)
    return service.refresh(refresh_token=payload.refresh_token)


@router.post("/logout", response_model=LogoutResponse)
def logout(payload: LogoutRequest | None = None, session=DatabaseSession) -> LogoutResponse:
    service = AuthService(session)
    service.logout(refresh_token=payload.refresh_token if payload else None)
    return LogoutResponse(detail="Logout completed successfully")


@router.get("/me", response_model=UserSummary)
def me(current_user: AuthenticatedUser = Depends(get_current_user)) -> UserSummary:
    return UserSummary.model_validate(current_user)


@router.patch("/change-password", response_model=AuthResponse)
def change_password(
    payload: ChangePasswordRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session=DatabaseSession,
) -> AuthResponse:
    service = AuthService(session)
    return service.change_password(
        user_id=current_user.id,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )