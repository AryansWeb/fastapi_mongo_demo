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
    prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}}
)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise EmailAlreadyRegistered()

    hashed_password = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    await user.insert()
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
