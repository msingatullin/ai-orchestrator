#!/bin/bash

set -e

echo "📁 Перехожу в папку проекта..."
cd ~/ai-orchestrator

echo "📦 Обновляю docker-compose.yml..."
cat <<EOF > docker-compose.yml
services:
  api:
    build:
      context: .
    command: ["./entrypoint.sh"]
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - db
    environment:
      - ENV=production
      - DATABASE_URL=postgresql://ai:ai@db:5432/ai
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app/backend
      - ./alembic:/app/alembic
      - ./alembic.ini:/app/alembic.ini
      - ./entrypoint.sh:/app/entrypoint.sh

  redis:
    image: redis:7-alpine

  db:
    image: postgres:15
    environment:
      POSTGRES_DB=ai
      POSTGRES_USER=ai
      POSTGRES_PASSWORD=ai
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
EOF

echo "🐳 Создаю Dockerfile..."
cat <<EOF > Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry && poetry install --no-root

COPY . /app
RUN chmod +x /app/entrypoint.sh
EOF

echo "🔧 Создаю entrypoint.sh..."
cat <<'EOF' > entrypoint.sh
#!/bin/sh
set -e

echo "⚙️  Running Alembic migrations..."
poetry run alembic upgrade head

echo "🚀 Starting Uvicorn..."
exec poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
EOF

chmod +x entrypoint.sh

echo "🧬 Создаю alembic.ini..."
cat <<EOF > alembic.ini
[alembic]
script_location = alembic

[loggers]
keys = root

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
EOF

echo "🔁 Перезапускаю проект..."
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d

echo "✅ Готово! Логи API:"
docker compose logs -n 50 api
