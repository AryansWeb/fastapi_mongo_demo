from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user_id
from app.dependencies.products import get_valid_product
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
    },
)


@router.get(
    "/",
    response_model=List[ProductOut],
    summary="Obtener todos los productos del usuario",
    description="Lista todos los productos creados por el usuario autenticado con filtros opcionales",
)
async def get_all_products(
    user_id: str = Depends(get_current_user_id),
    min_price: float = 0.0,
    max_price: float = 1000000.0,  # A large default value
    query: Optional[str] = None,
):
    """
    Obtiene todos los productos del usuario autenticado.

    - **min_price**: Filtrar productos con precio mayor o igual a este valor
    - **max_price**: Filtrar productos con precio menor o igual a este valor
    - **query**: Búsqueda de texto en nombre y descripción del producto

    Retorna una lista de productos que pertenecen al usuario autenticado.
    """
    find_query = {"user_created": user_id}
    if query:
        find_query["$text"] = {"$search": query}

    products = await Product.find(
        find_query,
        Product.price >= min_price,
        Product.price <= max_price,
    ).to_list()
    return products


@router.get(
    "/aggregation/by_user",
    response_model=dict,
    summary="Estadísticas de productos por usuario",
    description="Obtiene el conteo de productos agrupados por usuario",
)
async def aggregate_products_by_user():
    """
    Obtiene estadísticas de productos agrupados por usuario.

    Útil para análisis y reportes. Retorna el número de productos
    que ha creado cada usuario en el sistema.
    """
    pipeline = [
        {"$group": {"_id": "$user_created", "count": {"$sum": 1}}},
        {"$project": {"user_id": "$_id", "count": 1, "_id": 0}},
    ]
    result = await Product.get_pymongo_collection().aggregate(pipeline).to_list()

    return {"data": result}


@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
    description="Crea un nuevo producto asociado al usuario autenticado",
)
async def create_product(
    product_data: ProductCreate, user_id: str = Depends(get_current_user_id)
):
    """
    Crea un nuevo producto.

    - **name**: Nombre del producto (requerido)
    - **description**: Descripción opcional del producto
    - **price**: Precio del producto (debe ser mayor o igual a 0)

    El producto se asocia automáticamente al usuario autenticado.
    """
    product = Product(**product_data.model_dump(), user_created=user_id)
    await product.insert()
    return product


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Obtener producto por ID",
    description="Obtiene un producto específico por su ID (solo si pertenece al usuario)",
)
async def get_one_product(product: Product = Depends(get_valid_product)):
    """
    Obtiene un producto específico por su ID.

    Solo puede acceder el usuario que creó el producto.
    Si el producto no existe o no pertenece al usuario, se retorna un error.
    """
    return product


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Actualizar producto",
    description="Actualiza un producto existente (solo si pertenece al usuario)",
)
async def update_product(
    data: ProductUpdate, product: Product = Depends(get_valid_product)
):
    """
    Actualiza un producto existente.

    - Permite actualización parcial (solo los campos enviados se actualizan)
    - Solo puede actualizar el usuario que creó el producto
    - Actualiza automáticamente el campo updated_at con la fecha actual

    Los campos no enviados en la petición mantienen su valor actual.
    """
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    await product.set(update_data)
    updated_product = await Product.get(product.id)
    return updated_product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto existente (solo si pertenece al usuario)",
)
async def delete_product(product: Product = Depends(get_valid_product)):
    """
    Elimina un producto existente.

    - Solo puede eliminar el usuario que creó el producto
    - La eliminación es permanente y no se puede deshacer
    - Retorna status 204 (No Content) si la eliminación es exitosa
    """
    await product.delete()
    return None
