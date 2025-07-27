import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.digital_twin.services.digital_twin_service import DigitalTwinService
from backend.app.digital_twin.api import digital_twin as api_module
from backend.app.main import app, startup_event
from httpx import AsyncClient, ASGITransport
from fastapi_limiter import FastAPILimiter


@pytest.mark.asyncio
async def test_service_style_and_context():
    service = DigitalTwinService()
    twin = await service.create_digital_twin(uuid4(), "Tester")
    service.twins[twin.id].style_profile = {"tone": "friendly"}
    service.twins[twin.id].context_window = 2

    resp1 = await service.generate_response(twin.id, "Hi")
    assert resp1.endswith("ctx:1")
    assert "friendly" in resp1

    await service.generate_response(twin.id, "How are you?")
    resp3 = await service.generate_response(twin.id, "Tell me more")
    assert resp3.endswith("ctx:2")
    assert "friendly" in resp3


@pytest.mark.asyncio
async def test_api_style_and_context(monkeypatch):
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

        twin_uuid = UUID(twin_id)
        api_module.service.twins[twin_uuid].style_profile = {"tone": "friendly"}
        api_module.service.twins[twin_uuid].context_window = 2

        await ac.post(f"/digital-twin/{twin_id}/generate", params={"query": "Hi"})
        resp = await ac.post(f"/digital-twin/{twin_id}/generate", params={"query": "More"})
        assert resp.status_code == 200
        assert resp.json()["response"].endswith("ctx:2")
        assert "friendly" in resp.json()["response"]
