from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import (
    CredentialsException,
    EmailAlreadyRegistered,
    FieldRequired,
    FieldTooShort,
)
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserOut
from app.utils.auth_utils import create_access_token, hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
    },
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario con email y contraseña",
)
async def register(user_data: UserCreate):
    """
    Registra un nuevo usuario en el sistema.

    - **email**: Email único del usuario
    - **password**: Contraseña del usuario

    Retorna la información del usuario creado (sin la contraseña).
    """
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise EmailAlreadyRegistered()

    hashed_password = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    await user.insert()
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario y devuelve un token JWT",
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Inicia sesión con email y contraseña.

    - **username**: Email del usuario (se usa username por compatibilidad OAuth2)
    - **password**: Contraseña del usuario

    Retorna un token JWT para autenticación en endpoints protegidos.
    """
    if form_data.username is None:
        raise FieldRequired("username")
    if form_data.username == "":
        raise FieldTooShort("username")
    if form_data.password is None:
        raise FieldRequired("password")
    if form_data.password == "":
        raise FieldTooShort("password")
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise CredentialsException()

    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return Token(access_token=token)
