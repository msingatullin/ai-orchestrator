import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from httpx import AsyncClient, ASGITransport
from backend.app.config.database import Base, get_settings, engine as app_engine, SessionLocal
from backend.app.main import app, startup_event
from fastapi_limiter import FastAPILimiter

settings = get_settings()
settings.redis_url = ""
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = app_engine
TestingSessionLocal = SessionLocal

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
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


@pytest.mark.asyncio
async def test_users_me():
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

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/auth/register", json={"email": "b@b.com", "password": "pass"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        resp = await ac.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "b@b.com"
