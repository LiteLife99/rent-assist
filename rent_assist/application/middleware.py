import http
import logging
from time import time

from fastapi import Request


async def log_request_middleware(request: Request, call_next):
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    protocol = "HTTP/" + request.scope.get("http_version", "UNDEFINED")
    start_time = time()
    response = await call_next(request)
    process_time = (time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase = "-"
        log_format = (
            f'{host}:{port} - "{request.method}" "{url}" "{protocol}" '
            f'{response.status_code} "{status_phrase}" {formatted_process_time}'
        )
        logging.getLogger("uvicorn.customaccess").info(
            log_format,
            extra={
                "client_address": host,
                "x_forwarded_for": request.headers.get("x-forwarded-for", "-"),
                "x_real_ip": request.headers.get("x-real-ip", "-"),
                "method": request.method,
                "path": request.url.path,
                "query": request.query_params if request.query_params else {},
                "protocol": protocol,
                "status_code": response.status_code,
                "status_phrase": status_phrase,
                "process_time": formatted_process_time,
            },
        )

    return response
