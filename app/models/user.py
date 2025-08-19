from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """
    Modelo de usuario para autenticación y gestión de cuentas.

    Attributes:
        email: Email único del usuario (indexado)
        hashed_password: Contraseña hasheada con Argon2
        created_at: Fecha y hora de creación del usuario
    """

    email: Annotated[EmailStr, Indexed(unique=True)] = Field(
        ..., description="Email único del usuario"
    )
    hashed_password: str = Field(..., description="Contraseña hasheada con Argon2")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora de creación del usuario",
    )

    class Settings:
        name = "users"

    def __str__(self) -> str:
        return f"User(email={self.email})"

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, created_at={self.created_at})"
