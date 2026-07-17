import logging
import sys
from typing import Union

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, Response


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {
        "errors": exc.errors(),
        "query_params": query_params,
    }
    logging.getLogger("uvicorn.validation").info(detail, extra=detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    protocol = "HTTP/" + request.scope.get("http_version", "UNKNOWN")
    exception_details = "Internal Server Error "
    if isinstance(exc, ExceptionGroup):
        for e in exc.exceptions:
            exception_details += f"<{e.__class__.__name__}>: {str(e)}"
    else:
        exception_type, exception_value, _ = sys.exc_info()
        exception_name = getattr(exception_type, "__name__", None)
        exception_details += f"<{exception_name}>: {exception_value}"
    log_format = f'{host}:{port} - "{request.method}" "{url}" "{protocol}" 500 "{exception_details}" -'
    logging.getLogger("uvicorn.customaccess").error(
        log_format,
        extra={
            "client_address": host,
            "x_forwarded_for": request.headers.get("x-forwarded-for", "-"),
            "x_real_ip": request.headers.get("x-real-ip", "-"),
            "method": request.method,
            "path": request.url.path,
            "query": request.query_params if request.query_params else {},
            "protocol": protocol,
            "status_code": 500,
            "status_phrase": exception_details,
        },
    )
    response_body = "Internal Server Error"
    return PlainTextResponse(
        response_body,
        status_code=500,
        headers={"Content-length": str(len(response_body))},
    )
