import logging
from functools import lru_cache
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from rent_assist.application.config import Settings
from rent_assist.application.depends import Depends
from rent_assist.infra.db.postgresql.database import SQLDatabase
from rent_assist.infra.db.postgresql.repositories.demo_items_repository import DemoItemsRepository
from rent_assist.infra.db.postgresql.uow import AsyncSQLAlchemyUnitOfWork
from rent_assist.infra.jwt.utils import JWTUtils
from rent_assist.infra.redis.client import RedisClient
from rent_assist.modules.demo.service import DemoService

settings = Settings()
database = SQLDatabase(settings.POSTGRES_URL_UNICODE)

redis_client = RedisClient(settings.REDIS_URL)

jwt_utils = JWTUtils(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
)


@lru_cache
def di_get_settings() -> Settings:
    return Settings.get_settings()


@lru_cache
def di_get_logger() -> logging.Logger:
    import logging.config

    config_file = di_get_settings().LOGGING_CONFIG
    logging.config.fileConfig(config_file, disable_existing_loggers=False)
    logging.captureWarnings(True)
    return logging.getLogger()


def di_get_db():
    return database


async def di_get_session(
    db: Annotated[SQLDatabase, Depends(di_get_db)],
):
    async with db.session_maker() as session:
        yield session


async def di_get_uow(
    session: Annotated[AsyncSession, Depends(di_get_session)],
) -> AsyncSQLAlchemyUnitOfWork:
    return AsyncSQLAlchemyUnitOfWork(session=session)


async def di_get_redis_client() -> RedisClient:
    return redis_client


def di_get_jwt_utils() -> JWTUtils:
    return jwt_utils


async def di_get_demo_items_repository(
    session: Annotated[AsyncSession, Depends(di_get_session)],
) -> DemoItemsRepository:
    return DemoItemsRepository(session=session)


async def di_get_demo_service(
    demo_items_repository: Annotated[DemoItemsRepository, Depends(di_get_demo_items_repository)],
) -> DemoService:
    return DemoService(demo_items_repository=demo_items_repository)
