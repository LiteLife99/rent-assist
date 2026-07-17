from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from rent_assist.application.di.main import di_get_db, di_get_logger, redis_client
from rent_assist.application.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from rent_assist.application.middleware import log_request_middleware
from rent_assist.infra.exceptions.exception_handlers import error_handlers_map
from rent_assist.modules.demo.router import router as demo_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    logger = di_get_logger()
    db = di_get_db()
    try:
        try:
            await redis_client.connect()
            logger.info("Redis initialized successfully")
        except Exception as e:
            logger.warning(f"Redis initialization failed: {e}.")
        yield
    finally:
        await redis_client.disconnect()
        logger.info("Redis shut down successfully")
        if db:
            await db.shutdown()
            logger.info("Db shut down successfully")


def create_fastapi_app():
    app = FastAPI(
        title="rent_assist API",
        description="API for rent-assist backend",
        version="1.0.0",
        exception_handlers=error_handlers_map,
        lifespan=lifespan,
        docs_url="/docs",
    )

    router = APIRouter()
    router.include_router(demo_router, prefix="/api/v1/demo")

    app.include_router(router)

    app.middleware("http")(log_request_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app
