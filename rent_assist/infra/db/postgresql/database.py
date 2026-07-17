# ruff: noqa
"""
Database connection and session management.

This module provides the SQLAlchemy engine and session factory for the application,
configured with appropriate connection pooling and serialization settings.
"""

from functools import lru_cache, partial
from typing import ClassVar, Self

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from rent_assist.infra.exceptions.models import InternalError
from rent_assist.infra.utils.orjson_helpers import OrjsonHelpers


class SQLDatabase:
    _instance: ClassVar[Self | None] = None

    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        pool_size: int = 2,
        max_overflow: int = 20,
        pool_recycle: int = 3600,
    ):
        self.db_url = db_url
        self.echo = echo
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        SQLDatabase._instance = self

    @lru_cache(maxsize=1)  # noqa: B019
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            self.db_url,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_recycle=self.pool_recycle,
            json_serializer=partial(OrjsonHelpers.serialize, return_bytes=False),
        )

    @property
    @lru_cache(maxsize=1)  # noqa: B019
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self.get_engine(),
            autocommit=False,
            expire_on_commit=False,
        )

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            raise InternalError("SQLDatabase not initialized")
        return cls._instance

    async def shutdown(self):
        await self.get_engine().dispose()
