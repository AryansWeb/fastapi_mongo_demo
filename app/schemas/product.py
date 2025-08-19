from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Schema para crear un nuevo producto"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Gaming",
                "description": "Laptop para gaming con RTX 4060",
                "price": 1299.99,
            }
        }
    )

    name: str = Field(
        ..., min_length=1, max_length=100, description="Nombre del producto"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Descripción del producto"
    )
    price: float = Field(
        ...,
        ge=0,
        le=999999.99,
        description="Precio del producto (debe ser mayor o igual a 0)",
    )


class ProductUpdate(BaseModel):
    """Schema para actualizar un producto existente"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Gaming Actualizada",
                "description": "Nueva descripción del producto",
                "price": 1199.99,
            }
        }
    )

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Nombre del producto"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Descripción del producto"
    )
    price: Optional[float] = Field(
        None, ge=0, le=999999.99, description="Precio del producto"
    )


class ProductOut(BaseModel):
    """Schema para la respuesta de producto"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "Laptop Gaming",
                "description": "Laptop para gaming con RTX 4060",
                "price": 1299.99,
                "user_created": "507f1f77bcf86cd799439012",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T15:45:00Z",
            }
        },
    )

    id: PydanticObjectId = Field(..., description="ID único del producto")
    name: str = Field(..., description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., description="Precio del producto")
    user_created: str = Field(..., description="ID del usuario que creó el producto")
    created_at: datetime = Field(..., description="Fecha y hora de creación")
    updated_at: Optional[datetime] = Field(
        None, description="Fecha y hora de última actualización"
    )
