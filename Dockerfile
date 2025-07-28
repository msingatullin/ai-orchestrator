FROM python:3.11-slim

WORKDIR /app

# Copy project metadata including README before installing
COPY pyproject.toml poetry.lock* README.md /app/
# Install the project itself so that the `backend` package is available
RUN pip install --no-cache-dir poetry && poetry install

COPY . /app
RUN chmod +x /app/entrypoint.sh
