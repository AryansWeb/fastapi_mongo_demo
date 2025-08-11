from fastapi import HTTPException, status


class EmailAlreadyRegistered(HTTPException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TokenInvalid(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class FieldRequired(HTTPException):
    def __init__(self, field_name: str):
        detail = [
            {
                "loc": ["body", field_name],
                "msg": "field required",
                "type": "value_error",
            }
        ]
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class FieldTooShort(HTTPException):
    def __init__(self, field_name: str):
        detail = [
            {
                "loc": ["body", field_name],
                "msg": "ensure this value has at least 1 character",
                "type": "string_too_short",
            }
        ]
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class ProductNotFound(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ProductIdInvalid(HTTPException):
    def __init__(self, detail: str = "Invalid product id"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ProductAccessForbidden(HTTPException):
    def __init__(self, detail: str = "Access to this product is forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
