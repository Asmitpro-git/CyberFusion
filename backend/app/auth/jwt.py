from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal, TypedDict
from uuid import UUID

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config.settings import get_settings


TokenType = Literal["access", "refresh"]


class TokenData(TypedDict):
    user_id: str
    username: str
    role: str
    permissions: dict[str, Any]
    exp: int
    iat: int
    token_type: TokenType
    iss: str
    aud: str


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _create_token(*, subject: dict[str, Any], expires_delta: timedelta, token_type: TokenType) -> str:
    settings = get_settings()
    now = _utc_now()
    expire_at = now + expires_delta
    payload = {
        **subject,
        "token_type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire_at.timestamp()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(
    *,
    user_id: UUID,
    username: str,
    role: str,
    permissions: dict[str, Any],
) -> str:
    settings = get_settings()
    return _create_token(
        subject={
            "user_id": str(user_id),
            "username": username,
            "role": role,
            "permissions": permissions,
        },
        expires_delta=timedelta(minutes=settings.jwt_access_token_expire_minutes),
        token_type="access",
    )


def create_refresh_token(
    *,
    user_id: UUID,
    username: str,
    role: str,
    permissions: dict[str, Any],
) -> str:
    settings = get_settings()
    return _create_token(
        subject={
            "user_id": str(user_id),
            "username": username,
            "role": role,
            "permissions": permissions,
        },
        expires_delta=timedelta(days=settings.jwt_refresh_token_expire_days),
        token_type="refresh",
    )


def decode_token(token: str, *, verify_expiration: bool = True) -> TokenData:
    settings = get_settings()
    options = {"verify_exp": verify_expiration}
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options=options,
        )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    required_keys = {"user_id", "username", "role", "permissions", "exp", "iat", "token_type"}
    missing_keys = required_keys.difference(payload)
    if missing_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token payload",
        )

    token_type = payload.get("token_type")
    if token_type not in {"access", "refresh"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token type",
        )

    return {
        "user_id": str(payload["user_id"]),
        "username": str(payload["username"]),
        "role": str(payload["role"]),
        "permissions": dict(payload["permissions"]),
        "exp": int(payload["exp"]),
        "iat": int(payload["iat"]),
        "token_type": token_type,
        "iss": str(payload.get("iss", "")),
        "aud": str(payload.get("aud", "")),
    }


def verify_token(token: str, *, expected_type: TokenType | None = None) -> TokenData:
    payload = decode_token(token, verify_expiration=True)
    if expected_type is not None and payload["token_type"] != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unexpected authentication token type",
        )
    return payload