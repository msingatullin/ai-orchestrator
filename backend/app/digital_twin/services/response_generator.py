from __future__ import annotations

from typing import List, Dict

from .llm_service import LLMService
from ..models.digital_twin import DigitalTwin
from .prompt_engineer import PromptEngineer


class ResponseGenerator:
    """Generate responses for a digital twin using an LLM."""

    def __init__(self, llm: LLMService | None = None, prompter: PromptEngineer | None = None) -> None:
        self.llm = llm or LLMService()
        self.prompter = prompter or PromptEngineer()

    async def generate(self, twin: DigitalTwin, query: str, history: List[str]) -> str:
        messages = self.prompter.build_messages(twin, query, history)
        if self.llm.active:
            return await self.llm.generate(messages)
        tone = twin.style_profile.get("tone") if twin.style_profile else "neutral"
        return f"{twin.name} [{tone}] says: {query} | ctx:{len(history)}"
