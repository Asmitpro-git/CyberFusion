from __future__ import annotations

from fastapi import HTTPException, status


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not authorized") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)