from scalar_fastapi import get_scalar_api_reference

from rent_assist.application.app import create_fastapi_app

app = create_fastapi_app()


@app.get("/")
async def root():
    """Root endpoint for health checks."""
    return {"status": "ok", "message": "rent_assist API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "rent_assist API is running"}


@app.get("/scalar", include_in_schema=False)
def scalar_api():
    return get_scalar_api_reference(
        title=app.title,
        openapi_url=app.openapi_url,
    )
