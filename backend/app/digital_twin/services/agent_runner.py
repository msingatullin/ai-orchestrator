from __future__ import annotations

from uuid import UUID

from ..models.digital_twin import DigitalTwin
from .digital_twin_service import DigitalTwinService
from ...data_collection.nlp import NLPPipeline
from ...vector_db.services.search_service import SearchService
from ...vector_db.models.embeddings import MessageEmbedding
from ...data_collection.models.raw_data import RawMessage


class AgentRunner:
    """Run the full pipeline for a digital twin."""

    def __init__(self, twin_service: DigitalTwinService, search_service: SearchService | None = None) -> None:
        self.twin_service = twin_service
        self.search = search_service or SearchService()
        self.pipeline = NLPPipeline()

    async def handle_message(self, twin_id: UUID, message: RawMessage) -> str:
        processed = self.pipeline.process(message)
        embedding = MessageEmbedding(
            message_id=processed.raw_message_id,
            user_id=message.user_id,
            vector=self.search.embedder.encode_text(processed.cleaned_text),
        )
        self.search.add_message_embedding(embedding)
        _ = self.search.search_messages(message.user_id, processed.cleaned_text, limit=3)
        response = await self.twin_service.generate_response(twin_id, processed.cleaned_text)
        return response
