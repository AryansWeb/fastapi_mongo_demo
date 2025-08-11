import json
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.core.exception_handlers import (
    credentials_exception_handler,
    email_already_registered_exception_handler,
    exception_handler,
    field_required_exception_handler,
    field_too_short_exception_handler,
    http_exception_handler,
    product_access_forbidden_exception_handler,
    product_id_invalid_exception_handler,
    product_not_found_exception_handler,
    token_invalid_exception_handler,
)
from app.core.exceptions import (
    CredentialsException,
    EmailAlreadyRegistered,
    FieldRequired,
    FieldTooShort,
    ProductAccessForbidden,
    ProductIdInvalid,
    ProductNotFound,
    TokenInvalid,
)


@pytest.mark.anyio
class TestExceptionHandlers:
    async def test_email_already_registered_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = EmailAlreadyRegistered()
        response = await email_already_registered_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(response.body) == {"detail": "Email already registered"}

    async def test_credentials_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = CredentialsException()
        response = await credentials_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert json.loads(response.body) == {"detail": "Invalid credentials"}

    async def test_token_invalid_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = TokenInvalid()
        response = await token_invalid_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert json.loads(response.body) == {"detail": "Invalid token"}

    async def test_field_required_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = FieldRequired(field_name="email")
        response = await field_required_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert json.loads(response.body) == {
            "detail": [
                {
                    "loc": ["body", "email"],
                    "msg": "field required",
                    "type": "value_error",
                }
            ]
        }

    async def test_field_too_short_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = FieldTooShort(field_name="password")
        response = await field_too_short_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert json.loads(response.body) == {
            "detail": [
                {
                    "loc": ["body", "password"],
                    "msg": "ensure this value has at least 1 character",
                    "type": "string_too_short",
                }
            ]
        }

    async def test_product_not_found_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = ProductNotFound()
        response = await product_not_found_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert json.loads(response.body) == {"detail": "Product not found"}

    async def test_product_id_invalid_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = ProductIdInvalid()
        response = await product_id_invalid_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(response.body) == {"detail": "Invalid product id"}

    async def test_product_access_forbidden_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = ProductAccessForbidden()
        response = await product_access_forbidden_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert json.loads(response.body) == {
            "detail": "Access to this product is forbidden"
        }

    async def test_http_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="I'm a teapot"
        )
        response = await http_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT
        assert json.loads(response.body) == {"detail": "I'm a teapot"}

    async def test_http_exception_handler_no_detail(self):
        request = MagicMock(spec=Request)
        exc = HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=None)
        response = await http_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT
        assert json.loads(response.body) == {"detail": "I'm a Teapot"}

    async def test_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = ValueError("Something unexpected happened")
        response = await exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert json.loads(response.body) == {"detail": "Internal Server Error"}
