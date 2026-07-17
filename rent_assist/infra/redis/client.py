"""Redis client wrapper for async operations"""

import logging
from typing import ClassVar, Self

import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client wrapper"""

    _instance: ClassVar[Self | None] = None

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._client: aioredis.Redis | None = None
        RedisClient._instance = self

    async def connect(self):
        """Initialize Redis connection"""
        if self._client is None:
            self._client = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            logger.info("Redis client connected")

    async def disconnect(self):
        """Close Redis connection"""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Redis client disconnected")

    @property
    def client(self) -> aioredis.Redis:
        """Get Redis client instance"""
        if self._client is None:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._client

    @classmethod
    def get_instance(cls) -> Self:
        """Get singleton instance"""
        if cls._instance is None:
            raise RuntimeError("RedisClient not initialized")
        return cls._instance
