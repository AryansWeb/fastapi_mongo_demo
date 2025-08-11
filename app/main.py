from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.db.mongo import close_mongo_connection, connect_to_mongo
from app.models.product import Product
from app.models.user import User
from app.routes import auth, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    client, db = await connect_to_mongo()
    await init_beanie(database=db, document_models=[User, Product])
    app.state.mongo_client = client
    app.state.mongo_db = db
    yield
    await close_mongo_connection(client)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.api_version,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(products.router, prefix=settings.api_prefix)
