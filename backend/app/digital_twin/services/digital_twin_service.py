from __future__ import annotations

from typing import Dict, List
from uuid import UUID

from ..models.digital_twin import DigitalTwin, PersonalityProfile
from .llm_service import LLMService
from .feedback_handler import FeedbackHandler


class DigitalTwinService:
    """Manage Digital Twins in-memory."""

    def __init__(self, llm: LLMService | None = None, feedback: FeedbackHandler | None = None):
        self.twins: Dict[UUID, DigitalTwin] = {}
        self.profiles: Dict[UUID, PersonalityProfile] = {}
        self.memory: Dict[UUID, List[str]] = {}
        self.llm = llm or LLMService()
        self.feedback = feedback or FeedbackHandler()

    async def create_digital_twin(self, user_id: UUID, name: str) -> DigitalTwin:
        twin = DigitalTwin(user_id=user_id, name=name, status="ready")
        self.twins[twin.id] = twin
        self.profiles[twin.id] = PersonalityProfile(
            digital_twin_id=twin.id,
            description=f"Default personality for {name}",
        )
        self.memory[twin.id] = []
        return twin

    async def get_twin(self, twin_id: UUID) -> DigitalTwin:
        return self.twins[twin_id]

    async def generate_response(self, twin_id: UUID, query: str, rating: int | None = None) -> str:
        """Generate a response using the configured LLM and record feedback."""
        twin = await self.get_twin(twin_id)
        history = self.memory.setdefault(twin_id, [])
        history.append(query)
        recent = history[-twin.context_window :]

        messages: List[Dict[str, str]] = []
        persona = twin.persona_profile or self.profiles.get(twin_id).model_dump()
        if persona:
            desc = persona.get("description")
            if desc:
                messages.append({"role": "system", "content": desc})

        if twin.style_profile:
            style = ", ".join(f"{k}: {v}" for k, v in twin.style_profile.items())
            messages.append({"role": "system", "content": f"Style: {style}"})

        for text in recent:
            messages.append({"role": "user", "content": text})

        if self.llm.active:
            response = await self.llm.generate(messages)
        else:
            tone = twin.style_profile.get("tone") if twin.style_profile else "neutral"
            response = f"{twin.name} [{tone}] says: {query} | ctx:{len(recent)}"

        history.append(response)

        if rating is not None:
            await self.feedback.record_feedback(twin_id, response, rating)

        return response
