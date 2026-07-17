# Stage 1: Base image
FROM python:3.13-slim AS base

FROM base AS builder
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install git and build essentials for fetching and building dependencies
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_VERSION=3.13 \
    UV_PYTHON_DOWNLOADS=0

COPY ./pyproject.toml ./uv.lock ./alembic.ini ./migration.sh ./README.md ./uvicorn_logging_conf.ini ./uvicorn_logging_conf_string.ini ./scripts /app/
COPY ./rent_assist /app/rent_assist/
COPY ./migrations /app/migrations

# Fix line endings (CRLF -> LF) and make executable
RUN sed -i 's/\r$//' /app/migration.sh && chmod +x /app/migration.sh

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project


FROM builder AS prod

# Install vim and ensure it's available
RUN apt-get update && \
    apt-get install -y vim procps && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app
# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"
# Copy the application into the container.
COPY --from=builder /app /app

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync && \
    uv pip install .

# Run the application.
CMD ["uvicorn", "rent_assist.main:app", "--port", "8000", "--host", "0.0.0.0", "--reload", "--reload-dir", "/app/rent_assist", "--no-access-log", "--log-config=/app/uvicorn_logging_conf.ini"]

# Dev | Test
FROM prod AS dev

RUN uv sync --frozen --group dev --group test

# Run the application.
CMD ["uvicorn", "rent_assist.main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--reload-dir", "/app/rent_assist", "--no-access-log", "--log-config=/app/uvicorn_logging_conf.ini"]
