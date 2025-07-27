from __future__ import annotations

from typing import Dict
from uuid import UUID

from ..models.digital_twin import DigitalTwin, PersonalityProfile


class DigitalTwinService:
    """Manage Digital Twins in-memory."""

    def __init__(self):
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
        tone = twin.style_profile.get("tone") if twin.style_profile else "neutral"
        return f"{twin.name} [{tone}] says: {query} | ctx:{len(recent)}"
