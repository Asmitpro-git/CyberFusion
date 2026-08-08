from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import CurrentUser
from app.database.session import get_db
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

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)

    return service.register(
        username=request.username,
        email=request.email,
        password=request.password,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=200,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)

    return service.login(
        username_or_email=request.username_or_email,
        password=request.password,
    )


@router.post(
    "/refresh",
    response_model=AuthResponse,
    status_code=200,
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)

    return service.refresh(
        refresh_token=request.refresh_token,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=200,
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
) -> LogoutResponse:
    service = AuthService(db)

    service.logout(
        refresh_token=request.refresh_token,
    )

    return LogoutResponse(
        detail="Logged out successfully.",
    )


@router.get(
    "/me",
    response_model=UserSummary,
    status_code=200,
)
def get_me(
    current_user: CurrentUser,
) -> UserSummary:
    return UserSummary.model_validate(current_user)


@router.post(
    "/change-password",
    response_model=AuthResponse,
    status_code=200,
)
def change_password(
    request: ChangePasswordRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)

    return service.change_password(
        user_id=current_user.id,
        current_password=request.current_password,
        new_password=request.new_password,
    )