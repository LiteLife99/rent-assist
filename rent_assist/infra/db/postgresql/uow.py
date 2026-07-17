import logging
from typing import Any, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction


class AsyncSQLAlchemyUnitOfWork(AsyncContextManager):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._transaction: AsyncSessionTransaction | None = None
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self) -> None:
        self._transaction = self._session.begin()

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: Any,
    ) -> None:
        if exc_type is not None:
            self.logger.error(
                f"Transaction failed: {exc_value}, traceback: {traceback}",
                exc_info=True,
            )
            await self.rollback()
            raise exc_value

        else:
            try:
                await self.commit()
            except Exception as e:
                self.logger.error(f"Transaction failed: {e}", exc_info=True)
                await self.rollback()
                raise e

        await self._session.close()

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def transaction(self) -> AsyncSessionTransaction:
        return self._transaction

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
