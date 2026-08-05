from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.config.settings import get_settings
from app.schemas.token import TokenPayload

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.security import (
    ExpiredTokenError,
    InvalidTokenError,
    InvalidTokenTypeError,
)
from app.schemas.token import TokenPayload

settings = get_settings()


def _create_token(
    *,
    user_id: str,
    username: str,
    role: str,
    token_type: str,
    expires_delta: timedelta,
) -> str:
    """
    Internal helper for creating JWT tokens.
    """

    now = datetime.now(UTC)

    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "type": token_type,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + expires_delta,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(
    *,
    user_id: str,
    username: str,
    role: str,
) -> str:
    return _create_token(
        user_id=user_id,
        username=username,
        role=role,
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.jwt_access_token_expire_minutes,
        ),
    )


def create_refresh_token(
    *,
    user_id: str,
    username: str,
    role: str,
) -> str:
    return _create_token(
        user_id=user_id,
        username=username,
        role=role,
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.jwt_refresh_token_expire_days,
        ),
    )


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT.
    Returns a strongly typed TokenPayload.
    """

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )

    return TokenPayload.model_validate(payload)


def verify_token(
    token: str,
    *,
    token_type: str = "access",
) -> TokenPayload:
    """
    Verify token validity and expected type.
    """

    try:
        payload = decode_token(token)

        if payload.type != token_type:
            raise InvalidTokenTypeError(
                f"Expected '{token_type}' token but received '{payload.type}'."
            )

        return payload

    except ExpiredSignatureError as exc:
        raise ExpiredTokenError("Token has expired.") from exc

    except JWTError as exc:
        raise InvalidTokenError("Invalid JWT token.") from exc