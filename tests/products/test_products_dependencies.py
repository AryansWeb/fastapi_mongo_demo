from unittest.mock import AsyncMock

import pytest
from beanie import PydanticObjectId

from app.core.exceptions import ProductAccessForbidden, ProductNotFound
from app.dependencies.products import get_valid_product
from app.models.product import Product


@pytest.mark.anyio
class TestGetValidProduct:
    async def test_successfully(self, monkeypatch):
        mock_product = Product(
            id=PydanticObjectId(), name="Test", price=10.0, user_created="user1"
        )
        mock_get = AsyncMock(return_value=mock_product)
        monkeypatch.setattr(Product, "get", mock_get)

        result = await get_valid_product(mock_product.id, user_id="user1")

        assert result == mock_product
        mock_get.assert_called_once_with(mock_product.id)

    async def test_not_found(self, monkeypatch):
        mock_get = AsyncMock(return_value=None)
        monkeypatch.setattr(Product, "get", mock_get)
        product_id = PydanticObjectId()

        with pytest.raises(ProductNotFound):
            await get_valid_product(product_id, user_id="user1")

        mock_get.assert_called_once_with(product_id)

    async def test_forbidden(self, monkeypatch):
        mock_product = Product(
            id=PydanticObjectId(), name="Test", price=10.0, user_created="user2"
        )
        mock_get = AsyncMock(return_value=mock_product)
        monkeypatch.setattr(Product, "get", mock_get)

        with pytest.raises(ProductAccessForbidden):
            await get_valid_product(mock_product.id, user_id="user1")

        mock_get.assert_called_once_with(mock_product.id)
