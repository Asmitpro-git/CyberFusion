from __future__ import annotations


class AuthenticationError(Exception):
    """
    Base exception for all authentication-related errors.
    """


class InvalidTokenError(AuthenticationError):
    """
    Raised when a JWT is invalid or its signature cannot be verified.
    """


class ExpiredTokenError(AuthenticationError):
    """
    Raised when a JWT has expired.
    """


class InvalidTokenTypeError(AuthenticationError):
    """
    Raised when an access token is used where a refresh token is expected,
    or vice versa.
    """