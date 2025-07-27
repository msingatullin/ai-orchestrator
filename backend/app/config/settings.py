from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Agents Ecosystem"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379/0"
    llm_provider: str = "simple"
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()
