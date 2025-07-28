#!/bin/bash

set -e

echo "🚀 Установка Poetry..."
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

echo "✅ Проверка Poetry..."
poetry --version

echo "🔧 Обновление poetry.lock..."
cd ~/ai-orchestrator
poetry lock

echo "🛠️ Проверка alembic.ini..."
if [ ! -f "alembic.ini" ]; then
  echo "❗ Файл alembic.ini не найден, создаю..."
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
qualname =

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
EOF
else
  echo "✅ alembic.ini найден"
fi

echo "🐳 Docker Compose билд..."
docker compose down --remove-orphans
docker compose build --no-cache

echo "▶️ Запуск контейнеров..."
docker compose up -d

echo "📋 Логи API:"
sleep 2
docker compose logs -n 30 api
