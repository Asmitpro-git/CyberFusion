import pytest
from datetime import timedelta
from app.core.jwt import _create_token
from app.core.security import ExpiredTokenError
from app.core.security import InvalidTokenTypeError, InvalidTokenError
from app.core.jwt import create_access_token, create_refresh_token, decode_token, verify_token


def test_create_access_token():
    token = create_access_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    token = create_refresh_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

def test_decode_access_token():
    """
    Test decoding a valid access token.
    """

    token = create_access_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    payload = decode_token(token)

    assert payload.sub == "123"
    assert payload.username == "admin"
    assert payload.role == "Administrator"
    assert payload.type == "access"
    assert payload.iss is not None
    assert payload.aud is not None
    assert payload.jti is not None
    
def test_verify_access_token():
    """
    Test verifying a valid access token.
    """

    token = create_access_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    payload = verify_token(token)

    assert payload.sub == "123"
    assert payload.username == "admin"
    assert payload.role == "Administrator"
    assert payload.type == "access"

def test_verify_wrong_token_type():
    """
    A refresh token should not be accepted where an access token is expected.
    """

    refresh = create_refresh_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    with pytest.raises(InvalidTokenTypeError):
        verify_token(refresh)

def test_invalid_signature():
    """
    A modified JWT should be rejected.
    """

    token = create_access_token(
        user_id="123",
        username="admin",
        role="Administrator",
    )

    # Tamper with the JWT
    tampered = token + "abc"

    with pytest.raises(InvalidTokenError):
        verify_token(tampered)
        
def test_expired_token():
    """
    An expired token should be rejected.
    """

    token = _create_token(
        user_id="123",
        username="admin",
        role="Administrator",
        token_type="access",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(ExpiredTokenError):
        verify_token(token)