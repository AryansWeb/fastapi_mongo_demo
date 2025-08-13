from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user_id
from app.dependencies.products import get_valid_product
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[ProductOut])
async def get_all_products(
    user_id: str = Depends(get_current_user_id),
    min_price: float = 0.0,
    max_price: float = 1000000.0,  # A large default value
    query: Optional[str] = None,
):
    find_query = {"user_created": user_id}
    if query:
        find_query["$text"] = {"$search": query}

    products = await Product.find(
        find_query,
        Product.price >= min_price,
        Product.price <= max_price,
    ).to_list()
    return products


@router.get("/aggregation/by_user", response_model=dict)
async def aggregate_products_by_user():
    pipeline = [
        {"$group": {"_id": "$user_created", "count": {"$sum": 1}}},
        {"$project": {"user_id": "$_id", "count": 1, "_id": 0}},
    ]
    result = await Product.get_pymongo_collection().aggregate(pipeline).to_list()

    return {"data": result}


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, user_id: str = Depends(get_current_user_id)
):
    product = Product(**product_data.model_dump(), user_created=user_id)
    await product.insert()
    return product


@router.get("/{product_id}", response_model=ProductOut)
async def get_one_product(product: Product = Depends(get_valid_product)):
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    data: ProductCreate, product: Product = Depends(get_valid_product)
):
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    await product.set(update_data)
    updated_product = await Product.get(product.id)
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product: Product = Depends(get_valid_product)):
    await product.delete()
    return None
