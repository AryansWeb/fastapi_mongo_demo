from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings.

    Las variables se cargan desde variables de entorno o archivo .env
    """

    MONGO_URI: str
    MONGO_DB: str
    MONGO_DB_TEST: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PROJECT_NAME: str = "FastAPI MongoDB Demo"
    DESCRIPTION: str = (
        "API RESTful con autenticación JWT y gestión de productos usando MongoDB"
    )
    VERSION: str = "1"

    DOCS_URL: str = "/"
    REDOC_URL: str = "/redoc"

    ALLOWED_HOSTS: list[str] = ["*"]

    @property
    def api_prefix(self) -> str:
        """Prefijo para todas las rutas de la API"""
        return f"/api/v{self.VERSION}"

    @property
    def api_version(self) -> str:
        """Versión semántica de la API"""
        return f"{self.VERSION}.0.0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
