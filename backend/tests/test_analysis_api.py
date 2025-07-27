import sys
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_limiter import FastAPILimiter

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.main import app, startup_event
from backend.app.data_collection.models.processed_data import ProcessedMessage


@pytest.mark.asyncio
async def test_pipeline_and_style_endpoints():
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
        resp = await ac.post("/analysis/pipeline", json={"text": "Hello :)"})
        assert resp.status_code == 200
        processed = resp.json()
        assert processed["cleaned_text"].strip() == "Hello"

        msg = ProcessedMessage(
            raw_message_id=uuid4(),
            cleaned_text=processed["cleaned_text"],
            language="en",
            sentiment_score=processed["sentiment_score"],
            message_type="text",
            formality_level=processed["formality_level"],
            contains_emoji=processed["contains_emoji"],
            word_count=processed["word_count"],
        )
        def conv(v):
            if hasattr(v, "hex"):
                return str(v)
            if hasattr(v, "isoformat"):
                return v.isoformat()
            return v

        payload = {
            "messages": [{k: conv(v) for k, v in msg.model_dump().items()}],
            "user_id": str(uuid4()),
            "source": "test",
        }
        resp = await ac.post("/analysis/style", json=payload)
        assert resp.status_code == 200
        style = resp.json()
        assert style["avg_message_length"] > 0
