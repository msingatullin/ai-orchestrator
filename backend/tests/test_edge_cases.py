import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.digital_twin.services.llm_service import LLMService
from backend.app.vector_db.services.embedding_service import EmbeddingService


def test_embedding_service_fallback_empty_text():
    svc = EmbeddingService()
    vec = svc.encode_text("")
    assert len(vec) == svc.dimension


@pytest.mark.asyncio
async def test_llm_service_stub():
    llm = LLMService()
    assert not llm.active
    resp = await llm.generate([{"role": "user", "content": "ping"}])
    assert resp.startswith("[stub]")
