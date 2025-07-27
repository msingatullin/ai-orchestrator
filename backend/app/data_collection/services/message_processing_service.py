from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.raw_data import RawMessage
from ..models.processed_data import ProcessedMessage
from ..nlp import NLPPipeline


class MessageProcessingService:
    """Process raw messages using the NLP pipeline."""

    def __init__(self, db: Session, pipeline: NLPPipeline | None = None) -> None:
        self.db = db
        self.pipeline = pipeline or NLPPipeline()

    def process(self, message_id: str) -> ProcessedMessage:
        raw = self.db.query(RawMessage).filter(RawMessage.id == message_id).first()
        if not raw:
            raise ValueError("raw message not found")
        processed = self.pipeline.process(raw)
        return processed
