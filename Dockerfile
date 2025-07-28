FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-interaction --no-root
COPY backend /app/backend
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
