FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-interaction --no-root
COPY backend /app/backend
CMD ["poetry", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
