from contextlib import contextmanager
from enum import StrEnum
from typing import ClassVar, Self
from urllib.parse import quote

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(StrEnum):
    TEST = "test"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PROD = "production"


class Settings(BaseSettings):
    _instance: ClassVar[Self | None] = None

    model_config = SettingsConfigDict(env_file=".env", extra="allow", case_sensitive=True)

    @classmethod
    def get_settings(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    @contextmanager
    def override(cls, **kwargs):
        """Temporarily override settings for testing"""
        original = cls._instance
        cls._instance = cls(**kwargs)
        try:
            yield cls
        finally:
            cls._instance = original

    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    LOG_LEVEL: str = "INFO"

    STATIC_DIR_ABSOLUTE_PATH: str = "/app/rent_assist/static"
    LOGGING_CONFIG: str = "/app/uvicorn_logging_conf.ini"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{quote(self.REDIS_PASSWORD)}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.ENVIRONMENT == EnvironmentType.PROD and self.JWT_SECRET_KEY == "dev-secret-key-change-in-production":
            import warnings

            warnings.warn(
                "Using default JWT_SECRET_KEY in production! This is a security risk. "
                "Please set JWT_SECRET_KEY environment variable.",
                UserWarning,
                stacklevel=2,
            )

    @property
    def POSTGRES_URL_UNICODE(self):
        return self.POSTGRES_DSN.unicode_string()

    @computed_field
    @property
    def POSTGRES_DSN(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=quote(self.POSTGRES_USER),
            password=quote(self.POSTGRES_PASSWORD),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=quote(self.POSTGRES_DB),
        )
