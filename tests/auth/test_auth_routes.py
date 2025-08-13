from unittest.mock import MagicMock

import pytest

from app.core.exceptions import FieldRequired, FieldTooShort
from app.routes.auth import login


@pytest.mark.anyio
class TestRegister:
    async def test_register_user_integration(self, client):
        user_data = {"email": "integration@example.com", "password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "integration@example.com"

    async def test_register_user_failure(self, client):
        user_data = {"email": "duplicate@example.com", "password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Email already registered"

    async def test_register_with_invalid_email_format(self, client):
        user_data = {"email": "not-an-email", "password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    async def test_register_without_password(self, client):
        user_data = {"email": "no_password@example.com"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "missing" for error in data["detail"])

    async def test_register_without_email(self, client):
        user_data = {"password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "missing" for error in data["detail"])

    async def test_register_with_empty_email(self, client):
        user_data = {"email": "", "password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
        data = response.json()

        assert "detail" in data
        assert any(
            error["type"] == "value_error" and "email" in error["msg"].lower()
            for error in data["detail"]
        )

    async def test_register_with_empty_password(self, client):
        user_data = {"email": "empty_pass@example.com", "password": ""}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "string_too_short" for error in data["detail"])


@pytest.mark.anyio
class TestLogin:
    async def test_login_user_integration(self, client):
        user_data = {"email": "login@example.com", "password": "password123"}
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        login_data = {"username": "login@example.com", "password": "password123"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_with_invalid_email(self, client):
        login_data = {"username": "nonexistent@example.com", "password": "somepass"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"

    async def test_login_with_wrong_password(self, client):
        user_data = {"email": "wrongpass@example.com", "password": "correctpass"}
        await client.post("/api/v1/auth/register", json=user_data)
        login_data = {"username": "wrongpass@example.com", "password": "wrongpass"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"

    async def test_login_without_password(self, client):
        user_data = {
            "email": "login_no_password@example.com",
            "password": "password123",
        }
        await client.post("/api/v1/auth/register", json=user_data)
        login_data = {"username": "login_no_password@example.com"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "missing" for error in data["detail"])

    async def test_login_without_username(self, client):
        user_data = {
            "email": "login_no_username@example.com",
            "password": "password123",
        }
        await client.post("/api/v1/auth/register", json=user_data)
        login_data = {"password": "password123"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "missing" for error in data["detail"])

    async def test_login_with_empty_username(self, client):
        user_data = {
            "email": "login_empty_username@example.com",
            "password": "password123",
        }
        await client.post("/api/v1/auth/register", json=user_data)
        login_data = {"username": "", "password": "password123"}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "string_too_short" for error in data["detail"])

    async def test_login_with_empty_password(self, client):
        user_data = {
            "email": "login_empty_password@example.com",
            "password": "password123",
        }
        await client.post("/api/v1/auth/register", json=user_data)
        login_data = {"username": "login_empty_password@example.com", "password": ""}
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any(error["type"] == "string_too_short" for error in data["detail"])

    async def test_login_with_none_password_direct_call(self):
        mock_form_data = MagicMock()
        mock_form_data.username = "test@example.com"
        mock_form_data.password = None

        with pytest.raises(FieldRequired) as exc_info:
            await login(mock_form_data)

        assert "password" in str(exc_info.value)

        mock_form_data.password = ""

        with pytest.raises(FieldTooShort) as exc_info:
            await login(mock_form_data)

        assert "password" in str(exc_info.value)

    async def test_login_with_none_username_direct_call(self):
        mock_form_data = MagicMock()
        mock_form_data.username = None
        mock_form_data.password = "password123"

        with pytest.raises(FieldRequired) as exc_info:
            await login(mock_form_data)

        assert "username" in str(exc_info.value)

        mock_form_data.username = ""

        with pytest.raises(FieldTooShort) as exc_info:
            await login(mock_form_data)

        assert "username" in str(exc_info.value)
