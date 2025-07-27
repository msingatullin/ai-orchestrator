from __future__ import annotations

from typing import Dict
from uuid import UUID

from ..models.digital_twin import DigitalTwin, PersonalityProfile


class DigitalTwinService:
    """Manage Digital Twins in-memory."""

    def __init__(self):
        self.twins: Dict[UUID, DigitalTwin] = {}
        self.profiles: Dict[UUID, PersonalityProfile] = {}

    async def create_digital_twin(self, user_id: UUID, name: str) -> DigitalTwin:
        twin = DigitalTwin(user_id=user_id, name=name)
        twin.status = "ready"
        self.twins[twin.id] = twin
        self.profiles[twin.id] = PersonalityProfile(
            digital_twin_id=twin.id,
            description=f"Default personality for {name}",
        )
        return twin

    async def get_twin(self, twin_id: UUID) -> DigitalTwin:
        return self.twins[twin_id]

    async def generate_response(self, twin_id: UUID, query: str) -> str:
        twin = await self.get_twin(twin_id)
        # toy generation: echo query with name
        return f"{twin.name} says: {query}"
