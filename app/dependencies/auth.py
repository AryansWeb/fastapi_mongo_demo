from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import TokenInvalid

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_prefix}/auth/login",
    description="Token JWT de autenticación",
)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrae y valida el ID del usuario desde el token JWT.

    Args:
        token: Token JWT del header Authorization

    Returns:
        ID del usuario autenticado

    Raises:
        TokenInvalid: Si el token es inválido, expirado o no contiene user_id
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise TokenInvalid(detail="Token payload invalid")
        return user_id
    except JWTError:
        raise TokenInvalid(detail="Invalid token or expired token")
