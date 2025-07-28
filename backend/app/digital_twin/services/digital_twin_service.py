from __future__ import annotations

from typing import Dict, List
from uuid import UUID

from ..models.digital_twin import DigitalTwin, PersonalityProfile
from .llm_service import LLMService
from .feedback_handler import FeedbackHandler
from .response_generator import ResponseGenerator


class DigitalTwinService:
    """Manage Digital Twins in-memory."""

    def __init__(self, llm: LLMService | None = None, feedback: FeedbackHandler | None = None):
        self.twins: Dict[UUID, DigitalTwin] = {}
        self.profiles: Dict[UUID, PersonalityProfile] = {}
        self.memory: Dict[UUID, List[str]] = {}
        self.llm = llm or LLMService()
        self.feedback = feedback or FeedbackHandler()
        self.responder = ResponseGenerator(self.llm)

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

        response = await self.responder.generate(twin, query, recent)

        history.append(response)

        if rating is not None:
            await self.feedback.record_feedback(twin_id, response, rating)

        return response
