# rent-assist

Rent Assist Backend Service

## Setup

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- [uv](https://docs.astral.sh/uv/) package manager

### Quick Start

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

2. Start the services:
   ```bash
   make up
   ```

3. Run migrations:
   ```bash
   make setup
   ```

4. The API will be available at `http://localhost:8000`
   - Swagger docs: `http://localhost:8000/docs`
   - Scalar docs: `http://localhost:8000/scalar`

### Development

```bash
# Install dev dependencies
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Lint code
make lint

# Add a new migration
make add-migration message="your_migration_message"
```

### Project Structure

```
rent_assist/
├── application/          # App setup, config, DI, middleware
│   ├── app.py
│   ├── config.py
│   ├── depends.py
│   ├── di/main.py
│   ├── exception_handlers.py
│   └── middleware.py
├── infra/                # Infrastructure layer
│   ├── db/postgresql/    # Database (tables, mappers, repositories, UoW)
│   ├── exceptions/       # Error models and handlers
│   ├── jwt/              # JWT utilities
│   ├── redis/            # Redis client
│   └── utils/            # Shared utilities (orjson, retry)
├── modules/              # Business modules
│   └── demo/             # Demo module (data_models, dto, router, service, exceptions)
└── main.py               # FastAPI entry point
```
