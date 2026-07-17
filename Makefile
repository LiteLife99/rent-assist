.PHONY: test test-cov test-cov-html format lint lint-fix clean up up-interactive setup wipe install add-migration migrate-up migrate-down

.DEFAULT_GOAL := all

test: install-dev
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. uv run pytest tests

test-cov: install-dev
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. uv run pytest --cov=rent_assist --cov-report=term-missing tests

test-cov-html: install-dev
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. uv run pytest tests --cov=rent_assist --cov-report=html
	@echo "HTML coverage report generated in htmlcov/"

format:
	PYTHONDONTWRITEBYTECODE=1 uv run ruff format rent_assist

lint:
	PYTHONDONTWRITEBYTECODE=1 uv run ruff check rent_assist

lint-fix:
	PYTHONDONTWRITEBYTECODE=1 uv run ruff check rent_assist --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ dist/ build/ *.egg-info/

install-dev:
	PYTHONDONTWRITEBYTECODE=1 uv sync --group dev --group test

install:
	uv pip install -e ".[test]"

up:
	docker compose -f compose.yml up -d

up-interactive:
	docker compose -f compose.yml up

setup:
	make migrate-up

wipe:
	docker ps -aq | xargs docker rm -vf
	docker images -aq | xargs docker rmi -f
	docker volume ls -q | xargs docker volume rm
	echo "y" | docker system prune
	rm -rf .venv .uv.lock
	uv sync

add-migration:
	docker compose run --rm --service-ports web uv run alembic revision --autogenerate -m "$(message)"

migrate-up:
	docker exec rent-assist-web-1 uv run alembic upgrade head

migrate-down:
	docker exec rent-assist-web-1 uv run alembic downgrade -1

# Default target
all: format lint test test-cov
