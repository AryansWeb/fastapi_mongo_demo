from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.exceptions import DatabaseConnectionError
from app.db.mongo import close_mongo_connection, connect_to_mongo
from app.models.product import Product
from app.models.user import User
from app.routes import auth, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación FastAPI.

    Se ejecuta al inicio y al final de la aplicación para:
    - Conectar a MongoDB y configurar Beanie
    - Cerrar conexiones al finalizar
    """
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
    contact={
        "name": "Víctor García",
        "url": "https://github.com/vicogarcia16",
        "email": "mg_619@hotmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operaciones de autenticación y gestión de usuarios",
        },
        {
            "name": "products",
            "description": "Operaciones CRUD para productos",
        },
    ],
)

register_exception_handlers(app)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(products.router, prefix=settings.api_prefix)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint de verificación de salud de la aplicación.

    Verifica el estado de la aplicación y la conectividad con MongoDB.
    Útil para monitoreo, load balancers y verificación de despliegues.

    Returns:
        - 200: Aplicación y base de datos funcionando correctamente
        - 503: Problemas de conectividad o inicialización (DatabaseConnectionError)
    """
    if not hasattr(app.state, "mongo_client") or not app.state.mongo_client:
        raise DatabaseConnectionError("Database not initialized")

    try:
        await app.state.mongo_client.admin.command("ping")
    except Exception:
        raise DatabaseConnectionError("Database connection failed")

    return {
        "status": "healthy",
        "version": settings.api_version,
        "project": settings.PROJECT_NAME,
        "database": "connected",
    }
