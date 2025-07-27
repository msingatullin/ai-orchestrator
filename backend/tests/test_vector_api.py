import sys
from pathlib import Path
import pytest
from uuid import uuid4
from httpx import AsyncClient, ASGITransport
from fastapi_limiter import FastAPILimiter

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.main import app, startup_event
from backend.app.data_collection.models.processed_data import ProcessedMessage


@pytest.mark.asyncio
async def test_vector_api_index_and_search():
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
        user_id = uuid4()
        data = ProcessedMessage(
            raw_message_id=uuid4(),
            cleaned_text="hello world",
            language="en",
            sentiment_score=0.1,
            message_type="text",
            formality_level=0.1,
        )
        def conv(v):
            if hasattr(v, "hex"):
                return str(v)
            if hasattr(v, "isoformat"):
                return v.isoformat()
            return v

        payload = {k: conv(v) for k, v in data.model_dump().items()}
        resp = await ac.post("/vectors/index", json=payload, params={"user_id": str(user_id)})
        assert resp.status_code == 200
        emb_id = resp.json()["embedding_id"]

        resp = await ac.get("/vectors/search", params={"user_id": str(user_id), "query": "hello"})
        assert resp.status_code == 200
        assert emb_id in resp.json()["results"]
