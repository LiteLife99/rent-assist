import logging
from logging import Logger, getLogger
from typing import Callable, Optional, ParamSpec, TypeVar

from tenacity import (
    AsyncRetrying,
    after_log,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

P = ParamSpec("P")
T = TypeVar("T")


class RetryableError(Exception):
    """
    A wrapper exception that signals an operation should be retried.
    The original exception is preserved as the __cause__.
    """

    def __init__(self, message: str = "Retryable error occurred", original_exception: Optional[Exception] = None):
        super().__init__(message)
        if original_exception:
            self.__cause__ = original_exception


class Retrier:
    """
    A callable wrapper class that applies tenacity retry logic to function calls.
    By default, retries on RetryableError exception.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        multiplier: int = 1,
        min_wait: int = 2,
        max_wait: int = 10,
        retry_exceptions: tuple[type[Exception], ...] = (),
        logger: Optional[Logger] = None,
        log_level_before_sleep: str = "WARNING",
        log_level_after: str = "INFO",
        reraise: bool = True,
    ):
        self.max_attempts = max_attempts
        self.multiplier = multiplier
        self.min_wait = min_wait
        self.max_wait = max_wait

        self.retry_exceptions = (RetryableError,) + retry_exceptions
        self.logger = logger or getLogger(__name__)

        self.log_level_before_sleep = log_level_before_sleep
        self.log_level_after = log_level_after
        self.reraise = reraise

    def _create_async_retrying(self):
        log_level_before_sleep_int = getattr(logging, self.log_level_before_sleep.upper())
        log_level_after_int = getattr(logging, self.log_level_after.upper())

        return AsyncRetrying(
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(
                multiplier=self.multiplier,
                min=self.min_wait,
                max=self.max_wait,
            ),
            retry=retry_if_exception_type(self.retry_exceptions),
            before_sleep=before_sleep_log(self.logger, log_level_before_sleep_int),
            after=after_log(self.logger, log_level_after_int),
            reraise=self.reraise,
        )

    def _create_retry_decorator(self):
        log_level_before_sleep_int = getattr(logging, self.log_level_before_sleep.upper())
        log_level_after_int = getattr(logging, self.log_level_after.upper())

        return retry(
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(
                multiplier=self.multiplier,
                min=self.min_wait,
                max=self.max_wait,
            ),
            retry=retry_if_exception_type(self.retry_exceptions),
            before_sleep=before_sleep_log(self.logger, log_level_before_sleep_int),
            after=after_log(self.logger, log_level_after_int),
            reraise=self.reraise,
        )

    async def __call__(
        self,
        func: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        async_retrying = self._create_async_retrying()
        return await async_retrying(func, *args, **kwargs)

    def as_decorator(self):
        return self._create_retry_decorator()

    def context(self):
        return self._create_async_retrying()
