from beanie import PydanticObjectId
from fastapi import Depends

from app.core.exceptions import ProductAccessForbidden, ProductNotFound
from app.dependencies.auth import get_current_user_id
from app.models.product import Product


async def get_valid_product(
    product_id: PydanticObjectId, user_id: str = Depends(get_current_user_id)
) -> Product:
    product = await Product.get(product_id)
    if not product:
        raise ProductNotFound()
    if product.user_created != user_id:
        raise ProductAccessForbidden()
    return product
