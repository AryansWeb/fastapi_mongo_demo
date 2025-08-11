# conftest.py
import asyncio
from asyncio import SelectorEventLoop
from contextlib import asynccontextmanager

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


# === Fuerza SelectorEventLoop en Windows ===
@pytest.fixture(scope="function", autouse=True)
def event_loop():
    try:
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    except ImportError:
        pass

    loop = SelectorEventLoop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# === Desactiva lifespan de FastAPI ===
@asynccontextmanager
async def null_lifespan(app):
    yield


# === Cliente de prueba ===
@pytest.fixture(scope="function")
async def client():
    from app.main import app

    # Desactiva el lifespan
    app.router.lifespan_context = null_lifespan

    # Inicializa Beanie aquí (todo en el mismo loop)
    from beanie import init_beanie
    from httpx import ASGITransport, AsyncClient
    from motor.motor_asyncio import AsyncIOMotorClient

    from app.core.config import settings
    from app.models.product import Product
    from app.models.user import User

    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    test_db = mongo_client[settings.MONGO_DB_TEST]
    await init_beanie(database=test_db, document_models=[User, Product])

    # Limpia colección
    await User.find().delete_many()
    await Product.find().delete_many()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    # Limpieza
    await mongo_client.drop_database(settings.MONGO_DB_TEST)
    mongo_client.close()
