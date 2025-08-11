from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str
    MONGO_DB_TEST: str
    TESTING: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PROJECT_NAME: str = "FastAPI MongoDB Demo"
    DESCRIPTION: str = "Demo con autenticación y productos usando MongoDB y JWT"
    VERSION: str = "1"
    DOCS_URL: str = "/"
    REDOC_URL: str = "/redoc"

    @property
    def api_prefix(self):
        return f"/api/v{self.VERSION}"

    @property
    def api_version(self):
        return f"{self.VERSION}.0.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
