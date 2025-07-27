import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.config.database import Base
from backend.app.main import app, startup_event
from fastapi_limiter import FastAPILimiter
import os
from backend.app.config.database import get_settings

settings = get_settings()
settings.redis_url = ""
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_db():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_register_and_login():
    class DummyRedis:
        async def evalsha(self, *args, **kwargs):
            return None

    FastAPILimiter.redis = DummyRedis()
    async def ident(request):
        return "test"
    FastAPILimiter.identifier = ident
    async def cb(request, response, pexpire):
        return None
    FastAPILimiter.http_callback = cb
    await startup_event()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/auth/register", json={"email": "a@a.com", "password": "pass"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        refresh = resp.json()["refresh_token"]
        assert token and refresh

        resp = await ac.post("/auth/login", json={"email": "a@a.com", "password": "pass"})
        assert resp.status_code == 200
        assert resp.json()["refresh_token"]
        rt = resp.json()["refresh_token"]
        resp = await ac.post("/auth/refresh", params={"refresh_token": rt})
        assert resp.status_code == 200
        assert resp.json()["access_token"]
