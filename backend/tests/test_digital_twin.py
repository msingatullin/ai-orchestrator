import sys
from pathlib import Path

import pytest
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.digital_twin.services.digital_twin_service import DigitalTwinService
from httpx import AsyncClient, ASGITransport
from backend.app.main import app, startup_event
from fastapi_limiter import FastAPILimiter


@pytest.mark.asyncio
async def test_create_and_generate():
    service = DigitalTwinService()
    twin = await service.create_digital_twin(uuid4(), "Tester")
    assert twin.status == "ready"

    response = await service.generate_response(twin.id, "Hello")
    assert "Tester" in response


@pytest.mark.asyncio
async def test_api_endpoints():
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
        resp = await ac.post("/digital-twin/create", params={"user_id": user_id, "name": "Tester"})
        assert resp.status_code == 200
        twin_id = resp.json()["id"]

        resp = await ac.post(f"/digital-twin/{twin_id}/generate", params={"query": "hi"})
        assert resp.status_code == 200
        assert "Tester" in resp.json()["response"]
