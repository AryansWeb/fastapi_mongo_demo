from datetime import timedelta

from jose import jwt

from app.core.config import settings
from app.utils.auth_utils import (
    create_access_token,
    hash_password,
    verify_password,
)


class TestAuthUtils:
    def test_hash_password(self):
        password = "mysecretpassword"
        hashed_password = hash_password(password)

        assert hashed_password != password
        assert isinstance(hashed_password, str)
        assert verify_password(password, hashed_password)

    def test_verify_password_correct(self):
        password = "anothersecret"
        hashed_password = hash_password(password)
        assert verify_password(password, hashed_password)

    def test_verify_password_incorrect(self):
        password = "wrongpassword"
        hashed_password = hash_password("correctpassword")
        assert not verify_password(password, hashed_password)

    def test_create_access_token(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded_token["sub"] == data["sub"]
        assert "exp" in decoded_token

    def test_create_access_token_with_custom_expiry(self):
        data = {"sub": "test_expiry@example.com"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta=expires_delta)
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded_token["sub"] == data["sub"]
        assert "exp" in decoded_token
