#!/bin/sh
set -e

echo "⚙️  Running Alembic migrations..."
poetry run alembic upgrade head

echo "🚀 Starting Uvicorn..."
exec poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
