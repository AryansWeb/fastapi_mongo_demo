from datetime import datetime, timezone
from typing import Annotated, Optional

from beanie import Document, Indexed
from pydantic import Field, validator


class Product(Document):
    """
    Modelo de producto para el sistema de gestión de inventario.

    Attributes:
        name: Nombre del producto
        description: Descripción opcional del producto
        price: Precio del producto (debe ser positivo)
        user_created: ID del usuario que creó el producto (indexado)
        created_at: Fecha y hora de creación
        updated_at: Fecha y hora de última actualización
    """

    name: str = Field(
        ..., min_length=1, max_length=100, description="Nombre del producto"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Descripción opcional del producto"
    )
    price: float = Field(
        ..., ge=0, description="Precio del producto (debe ser mayor o igual a 0)"
    )
    user_created: Annotated[str, Indexed()] = Field(
        ..., description="ID del usuario que creó el producto"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora de creación del producto",
    )
    updated_at: Optional[datetime] = Field(
        None, description="Fecha y hora de última actualización"
    )

    class Settings:
        name = "products"
        indexes = [
            [
                ("name", "text"),
                ("description", "text"),
            ]
        ]

    @validator("price")
    def validate_price(cls, v):
        """Valida que el precio sea un número positivo"""
        if v < 0:
            raise ValueError("El precio debe ser mayor o igual a 0")
        return v

    def __str__(self) -> str:
        return f"Product(name={self.name}, price=${self.price})"

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, price={self.price}, user_created={self.user_created})"
