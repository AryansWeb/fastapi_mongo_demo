from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


async def connect_to_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    return client, db


async def close_mongo_connection(client):
    if client:
        client.close()
