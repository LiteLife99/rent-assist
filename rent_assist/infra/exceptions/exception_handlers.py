import logging
from typing import TypeVar

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError as PydanticValidationError

from rent_assist.infra.exceptions.models import InternalError, RentAssistError, ValidationError
from rent_assist.infra.exceptions.utils import get_log_message, loc_to_dot_sep


async def default_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    logging.error(
        get_log_message(request, exc, "500 - Internal Server Error"),
        exc_info=exc,
    )

    return ORJSONResponse(status_code=500, content=InternalError().model_dump())


async def rent_assist_error_handler(request: Request, exc: RentAssistError) -> ORJSONResponse:
    logging.error(
        get_log_message(request, exc, exc.model_dump()),
        exc_info=exc,
    )
    return ORJSONResponse(status_code=exc.status_code, content=exc.model_dump())


async def pydantic_error_handler(
    request: Request, exc: PydanticValidationError | RequestValidationError
) -> ORJSONResponse:
    error_message = ", ".join(
        [
            f"{error.get('msg')} (field={loc_to_dot_sep(error.get('loc'))}) (input={error.get('input')})"
            for error in exc.errors()
        ]
    )
    logging.error(
        get_log_message(request, exc, f"Pydantic error: {error_message}"),
        exc_info=exc,
    )
    if isinstance(exc, RequestValidationError):
        return ORJSONResponse(
            status_code=400,
            content=ValidationError(message=error_message).model_dump(),
        )
    return ORJSONResponse(status_code=500, content=InternalError().model_dump())


E = TypeVar("E", bound=Exception)

error_handlers_map = {
    RentAssistError: rent_assist_error_handler,
    PydanticValidationError: pydantic_error_handler,
    RequestValidationError: pydantic_error_handler,
    Exception: default_exception_handler,
}
