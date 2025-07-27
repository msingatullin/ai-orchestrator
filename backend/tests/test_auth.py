import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.config.database import Base
from backend.app.main import app
from backend.app.config.database import get_settings

settings = get_settings()
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/auth/register", json={"email": "a@a.com", "password": "pass"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token

        resp = await ac.post("/auth/login", json={"email": "a@a.com", "password": "pass"})
        assert resp.status_code == 200
        assert resp.json()["access_token"]
