from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


async def connect_to_mongo() -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    """Establece conexión con MongoDB usando Motor (driver asíncrono)."""
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    return client, db


async def close_mongo_connection(client: AsyncIOMotorClient) -> None:
    """Cierra la conexión con MongoDB de forma segura."""
    if client:
        client.close()
