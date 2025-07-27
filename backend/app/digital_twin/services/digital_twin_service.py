from __future__ import annotations

from typing import Dict
from uuid import UUID

from ...config.settings import get_settings
from ..models.digital_twin import DigitalTwin, PersonalityProfile
from .llm_backends import get_backend


class DigitalTwinService:
    """Manage Digital Twins in-memory."""

    def __init__(self, llm_provider: str | None = None):
        settings = get_settings()
        self.default_provider = llm_provider or settings.llm_provider
        self.twins: Dict[UUID, DigitalTwin] = {}
        self.profiles: Dict[UUID, PersonalityProfile] = {}
        self.memory: Dict[UUID, list[str]] = {}

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

    async def generate_response(self, twin_id: UUID, query: str) -> str:
        twin = await self.get_twin(twin_id)
        self.memory.setdefault(twin_id, []).append(query)
        recent = self.memory[twin_id][-twin.context_window :]
        profile = self.profiles.get(twin_id)
        tone = twin.style_profile.get("tone") if twin.style_profile else "neutral"

        prompt = "\n".join(
            [
                f"Personality: {profile.description if profile else ''}",
                f"Tone: {tone}",
                "Recent conversation:",
                *recent,
                f"User: {query}",
                f"{twin.name}:",
            ]
        )

        backend = get_backend(twin.llm_backend or self.default_provider)
        response = await backend.generate(
            prompt,
            twin=twin,
            query=query,
            recent=recent,
            tone=tone,
            profile=profile,
        )
        self.memory[twin_id].append(response)
        return response
