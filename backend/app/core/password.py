from __future__ import annotations

import re

from passlib.context import CryptContext

# Configure Passlib to use bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# Password Policy
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128

COMMON_PASSWORDS = {
    "password",
    "password123",
    "12345678",
    "123456789",
    "qwerty",
    "admin",
    "letmein",
}


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against its bcrypt hash.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    Determine whether a stored password hash should be upgraded.
    """
    return pwd_context.needs_update(hashed_password)


def validate_password_strength(password: str) -> None:
    """
    Validate password strength.

    Raises:
        ValueError
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    if password.strip() != password:
        raise ValueError("Password cannot start or end with spaces.")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must contain at least {MIN_PASSWORD_LENGTH} characters."
        )

    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters."
        )

    if password.lower() in COMMON_PASSWORDS:
        raise ValueError("Password is too common.")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain an uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain a lowercase letter.")

    if not re.search(r"\d", password):
        raise ValueError("Password must contain a number.")

    if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]", password):
        raise ValueError("Password must contain a special character.")