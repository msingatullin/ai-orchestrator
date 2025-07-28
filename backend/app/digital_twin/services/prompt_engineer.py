from __future__ import annotations

from typing import Dict, List

from ..models.digital_twin import DigitalTwin


class PromptEngineer:
    """Build structured prompts for the LLM from twin data and user query."""

    def build_messages(
        self, twin: DigitalTwin, query: str, history: List[str] | None = None
    ) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        persona = twin.persona_profile
        if not persona:
            persona = None
        if persona:
            desc = persona.get("description") if isinstance(persona, dict) else None
            if desc:
                messages.append({"role": "system", "content": desc})
        if twin.style_profile:
            style = ", ".join(f"{k}: {v}" for k, v in twin.style_profile.items())
            messages.append({"role": "system", "content": f"Style: {style}"})
        if history:
            for text in history:
                messages.append({"role": "user", "content": text})
        messages.append({"role": "user", "content": query})
        return messages
