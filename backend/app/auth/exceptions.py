from __future__ import annotations

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    def __init__(self, detail: str, *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(status_code=status_code, detail=detail)


class DuplicateEmailError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Email already exists", status_code=status.HTTP_409_CONFLICT)


class DuplicateUsernameError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Username already exists", status_code=status.HTTP_409_CONFLICT)


class WeakPasswordError(AuthenticationError):
    def __init__(self, detail: str = "Password does not meet the security policy") -> None:
        super().__init__(detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class InactiveAccountError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Account is inactive", status_code=status.HTTP_403_FORBIDDEN)


class LockedAccountError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Account is locked", status_code=status.HTTP_423_LOCKED)


class WrongPasswordError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidRefreshTokenError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Invalid refresh token", status_code=status.HTTP_401_UNAUTHORIZED)