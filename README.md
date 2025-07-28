# AI-Orchestrator

Пример базового модуля Core Platform на FastAPI. Запуск локально:

```bash
docker-compose up --build
```

После запуска приложение будет доступно на `http://localhost:8000` и содержит
эндпоинты аутентификации `/auth/register`, `/auth/login` и `/auth/refresh`.
Миграции выполняются через Alembic (`poetry run alembic upgrade head`).
Добавлены модели организаций и API-ключей, поддержка refresh токенов, базовый
RBAC по роли пользователя и ограничение частоты запросов через Redis.

Модуль цифровых двойников теперь поддерживает интеграцию с LLM (OpenAI).
При отсутствии API-ключа используется безопасная заглушка.
Для активации реального генератора необходимо установить переменную
`OPENAI_API_KEY`.

Healthcheck доступен на `/health`, метрики Prometheus на `/metrics`.

## Дополнительные возможности

- Встроенный Swagger UI доступен на `/docs` для интерактивного тестирования API.
- Запущен Celery брокер для асинхронных задач (`backend/app/tasks.py`). Пример задачи `generate_async` генерирует ответ от цифрового двойника во внешнем воркере.

## Запуск в staging

Для приближенного к продакшену окружения используется отдельный профиль Compose и прокси Nginx. Перед запуском выполните настройку переменных в `.env.production`.

```bash
docker compose --profile staging -f docker-compose.yml -f docker-compose.staging.yml up --build
```

При старте контейнера автоматически выполняются Alembic миграции, а Nginx доступен на порту 80.
