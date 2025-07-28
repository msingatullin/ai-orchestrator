FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
# Install the project itself so that the `backend` package is available
RUN pip install --no-cache-dir poetry && poetry install

COPY . /app
RUN chmod +x /app/entrypoint.sh
