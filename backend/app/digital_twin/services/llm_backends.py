from __future__ import annotations

import asyncio
import os
from typing import Any

try:  # pragma: no cover - optional dependency
    import openai
except Exception:  # pragma: no cover - if import fails fall back to simple backend
    openai = None


class LLMBackend:
    """Base interface for text generation backends."""

    async def generate(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class SimpleBackend(LLMBackend):
    """Trivial backend that echoes the last user message."""

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        twin = kwargs.get("twin")
        query = kwargs.get("query", "")
        tone = kwargs.get("tone", "neutral")
        recent = kwargs.get("recent", [])
        await asyncio.sleep(0)
        name = twin.name if twin else "Twin"
        return f"{name} [{tone}] says: {query} | ctx:{len(recent)}"


class OpenAIBackend(LLMBackend):
    """Backend using OpenAI's chat completion API."""

    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str | None = None) -> None:
        if openai is None:
            raise RuntimeError("openai package not installed")
        self.model = model
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        resp = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()


def get_backend(name: str) -> LLMBackend:
    name = (name or "simple").lower()
    if name == "openai" and openai is not None:
        try:
            return OpenAIBackend()
        except Exception:
            pass
    return SimpleBackend()
