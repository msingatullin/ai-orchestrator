import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.config.database import Base
from backend.app.main import app, startup_event
from fastapi_limiter import FastAPILimiter
from backend.app.config.database import get_settings
from backend.app.data_collection.nlp import NLPPipeline, StyleAnalyzer
from backend.app.data_collection.models.raw_data import RawMessage
from datetime import datetime

settings = get_settings()
settings.redis_url = ""
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_db():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_email_ingest_and_pipeline():
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
        payload = {
            "id": "1",
            "body": "I love this product!",
            "date": datetime.utcnow().isoformat(),
        }
        resp = await ac.post("/data-collection/email", json=payload, params={"user_id": "u1"})
        assert resp.status_code == 200
        message_id = resp.json()["id"]

        resp = await ac.post(f"/data-collection/process/{message_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["sentiment_score"] > 0

def test_style_analyzer():
    msgs = [
        RawMessage(
            id="11111111-1111-1111-1111-111111111111",
            user_id="11111111-1111-1111-1111-111111111111",
            organization_id=None,
            source="telegram",
            source_id="1",
            raw_content="Thanks!",
            message_metadata={},
            timestamp=datetime.utcnow(),
            is_outgoing=False,
            conversation_id="c1",
        ),
        RawMessage(
            id="22222222-2222-2222-2222-222222222222",
            user_id="11111111-1111-1111-1111-111111111111",
            organization_id=None,
            source="telegram",
            source_id="2",
            raw_content="Hello :)",
            message_metadata={},
            timestamp=datetime.utcnow(),
            is_outgoing=False,
            conversation_id="c1",
        ),
    ]
    pipeline = NLPPipeline()
    processed = [pipeline.process(m) for m in msgs]
    analyzer = StyleAnalyzer()
    style = analyzer.analyze(
        processed,
        user_id="11111111-1111-1111-1111-111111111111",
        source="telegram",
    )
    assert style.avg_message_length > 0
    assert style.dominant_sentiment in {"positive", "neutral", "negative"}
    assert style.sentiment_distribution
    assert style.emotion_patterns == {}

