from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    CredentialsException,
    EmailAlreadyRegistered,
    FieldRequired,
    FieldTooShort,
    ProductAccessForbidden,
    ProductIdInvalid,
    ProductNotFound,
    TokenInvalid,
)


async def email_already_registered_exception_handler(
    request: Request, exc: EmailAlreadyRegistered
):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def credentials_exception_handler(request: Request, exc: CredentialsException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def token_invalid_exception_handler(request: Request, exc: TokenInvalid):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def field_required_exception_handler(request: Request, exc: FieldRequired):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def field_too_short_exception_handler(request: Request, exc: FieldTooShort):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def product_id_invalid_exception_handler(request: Request, exc: ProductIdInvalid):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def product_not_found_exception_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def product_access_forbidden_exception_handler(
    request: Request, exc: ProductAccessForbidden
):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail or "HTTP Error"}
    )


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        EmailAlreadyRegistered, email_already_registered_exception_handler
    )
    app.add_exception_handler(CredentialsException, credentials_exception_handler)
    app.add_exception_handler(TokenInvalid, token_invalid_exception_handler)
    app.add_exception_handler(FieldRequired, field_required_exception_handler)
    app.add_exception_handler(FieldTooShort, field_too_short_exception_handler)
    app.add_exception_handler(ProductIdInvalid, product_id_invalid_exception_handler)
    app.add_exception_handler(ProductNotFound, product_not_found_exception_handler)
    app.add_exception_handler(
        ProductAccessForbidden, product_access_forbidden_exception_handler
    )
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, exception_handler)
