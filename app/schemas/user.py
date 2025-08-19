from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema para crear un nuevo usuario"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "usuario@ejemplo.com", "password": "mipassword123"}
        }
    )

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(
        ..., min_length=1, max_length=100, description="Contraseña del usuario"
    )


class UserOut(BaseModel):
    """Schema para la respuesta de usuario (sin contraseña)"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "usuario@ejemplo.com",
            }
        },
    )

    id: PydanticObjectId = Field(..., description="ID único del usuario")
    email: EmailStr = Field(..., description="Email del usuario")


class Token(BaseModel):
    """Schema para el token de autenticación"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )

    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
