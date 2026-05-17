from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================
    # APP
    # =========================================================

    APP_NAME: str = "Enterprise AI Knowledge Assistant"
    APP_VERSION: str = "0.1.0"

    ENVIRONMENT: Literal["development", "production", "test"] = "development"

    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"

    # =========================================================
    # SERVER
    # =========================================================

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # =========================================================
    # DATABASE
    # =========================================================

    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/eai_ka"
    )

    # =========================================================
    # REDIS
    # =========================================================

    REDIS_URL: str = "redis://localhost:6379"

    # =========================================================
    # JWT
    # =========================================================

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600

    # =========================================================
    # VECTOR DATABASE
    # =========================================================

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # =========================================================
    # LLM PROVIDERS
    # =========================================================

    OPENAI_API_KEY: str | None = None
    MISTRAL_API_KEY: str | None = None

    # =========================================================
    # EMBEDDINGS
    # =========================================================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en"

    # =========================================================
    # LOGGING
    # =========================================================

    LOG_LEVEL: str = "INFO"

    # =========================================================
    # MONITORING
    # =========================================================

    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = True

    # =========================================================
    # FILE UPLOAD
    # =========================================================

    MAX_UPLOAD_SIZE_MB: int = 50

    ALLOWED_EXTENSIONS: list[str] = [
        ".pdf",
        ".docx",
        ".txt",
        ".md",
    ]

    # =========================================================
    # COMPUTED PROPERTIES
    # =========================================================

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == "test"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()


settings = get_settings()
