from datetime import datetime, timezone
from typing import Annotated, Optional

from beanie import Document, Indexed
from pydantic import Field


class Product(Document):
    name: str
    description: Optional[str] = None
    price: float
    user_created: Annotated[str, Indexed()]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "products"
        indexes = [
            [
                ("name", "text"),
                ("description", "text"),
            ]
        ]
