#!/bin/bash

# Script to manually run database migrations
# Usage: ./run_migrations.sh

set -e

echo "========================================="
echo "Running Database Migrations"
echo "========================================="

# Check if running in docker or locally
if [ -f /.dockerenv ] || [ -n "$DOCKER_CONTAINER" ]; then
    echo "Running inside Docker container..."
    python -m alembic upgrade head
else
    echo "Running on host machine..."
    echo "Make sure you have:"
    echo "  1. Database connection configured in .env"
    echo "  2. Python environment activated"
    echo "  3. All dependencies installed"
    echo ""
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python -m alembic upgrade head
    else
        echo "Migration cancelled."
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "Migration Status:"
echo "========================================="
python -m alembic current

echo ""
echo "Migrations completed!"
