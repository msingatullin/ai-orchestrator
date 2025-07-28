from __future__ import annotations

import asyncio
import logging
import os
from typing import List, Dict

try:
    import openai
except Exception:  # pragma: no cover - openai optional
    openai = None

logger = logging.getLogger(__name__)


class LLMService:
    """Wrapper around OpenAI chat completions with graceful fallback."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.model = model
        self.active = False
        if openai is not None and os.environ.get("OPENAI_API_KEY"):
            openai.api_key = os.environ["OPENAI_API_KEY"]
            self.active = True
        else:
            if openai is None:
                logger.warning("openai package not available, using stub responses")
            else:
                logger.warning("OPENAI_API_KEY not set, using stub responses")

    async def generate(self, messages: List[Dict[str, str]]) -> str:
        if self.active:
            try:
                # use thread executor for sync API to avoid blocking
                loop = asyncio.get_event_loop()
                resp = await loop.run_in_executor(
                    None,
                    lambda: openai.ChatCompletion.create(model=self.model, messages=messages),
                )
                return resp["choices"][0]["message"]["content"]
            except Exception as exc:  # pragma: no cover - network/runtime issues
                logger.warning("OpenAI generation failed: %s", exc)
        # fallback behaviour mirrors previous placeholder implementation
        user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return f"[stub] {user_msg}"
