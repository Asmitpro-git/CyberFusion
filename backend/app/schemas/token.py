from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    Response returned after successful authentication.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class TokenPayload(BaseModel):
    """
    JWT payload after decoding and validation.
    """

    sub: str
    username: str
    role: str
    type: str
    jti: str

    iss: str
    aud: str

    iat: datetime
    exp: datetime

    model_config = ConfigDict(from_attributes=True)