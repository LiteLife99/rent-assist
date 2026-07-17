from abc import ABC
from typing import Any, Literal

from pydantic import RootModel
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class RentAssistError(Exception, ABC):
    message: str
    error_code: str | None = None
    status_code: int = 500
    detail: Any = None

    def model_dump(self) -> dict:
        return RootModel[self.__class__](self).model_dump()


@dataclass(slots=True)
class ValidationError(RentAssistError):
    status_code: Literal[400] = 400


@dataclass(slots=True)
class UnauthorizedError(RentAssistError):
    message: str = "Unauthorized"
    status_code: Literal[401] = 401


@dataclass(slots=True)
class ForbiddenError(RentAssistError):
    message: str = "Forbidden"
    status_code: Literal[403] = 403


@dataclass(slots=True)
class NotFoundError(RentAssistError):
    message: str = "Not Found"
    status_code: Literal[404] = 404


@dataclass(slots=True)
class InternalError(RentAssistError):
    message: str = "Internal Server Error"
    status_code: Literal[500] = 500
