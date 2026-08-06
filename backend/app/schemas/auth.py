from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RoleSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    permissions: dict[str, object]
    created_at: datetime


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    role: RoleSummary
    is_active: bool
    is_verified: bool
    failed_login_attempts: int
    locked_until: datetime | None = None
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime


class RegisterRequest(BaseModel):
    """
    Request schema for user registration.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["asmit"],
    )

    email: EmailStr = Field(
        ...,
        examples=["asmit@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["CyberFusion@2026"],
    )


class UserResponse(BaseModel):
    """
    Public user information.
    """

    id: str
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class RegisterResponse(BaseModel):
    """
    Response returned after successful registration.
    """

    message: str
    user: UserResponse


class LoginRequest(BaseModel):
    username_or_email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class AuthResponse(BaseModel):
    tokens: AuthTokenResponse
    user: UserSummary


class LogoutResponse(BaseModel):
    detail: str
