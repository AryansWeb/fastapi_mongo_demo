import pytest
from jose import jwt

from app.core.config import settings
from app.core.exceptions import TokenInvalid
from app.dependencies.auth import get_current_user_id
from app.utils.auth_utils import create_access_token


@pytest.mark.anyio
class TestGetCurrentUserId:
    async def test_successfully(self):
        user_id = "test_user_id"
        token = create_access_token(data={"sub": user_id})
        result_user_id = await get_current_user_id(token)
        assert result_user_id == user_id

    async def test_invalid_token(self):
        with pytest.raises(TokenInvalid) as exc_info:
            await get_current_user_id("invalid_token")
        assert "Invalid token or expired token" in str(exc_info.value)

    async def test_missing_sub(self):
        token = jwt.encode({}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        with pytest.raises(TokenInvalid) as exc_info:
            await get_current_user_id(token)
        assert "Token payload invalid" in str(exc_info.value)

    async def test_sub_is_none(self):
        token = create_access_token(data={"sub": None})
        with pytest.raises(TokenInvalid) as exc_info:
            await get_current_user_id(token)
        assert "Invalid token or expired token" in str(exc_info.value)
