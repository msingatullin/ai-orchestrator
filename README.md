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
