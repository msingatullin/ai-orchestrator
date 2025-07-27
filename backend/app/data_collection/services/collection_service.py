from __future__ import annotations

from uuid import uuid4
from sqlalchemy.orm import Session

from ..models.raw_data import RawMessage
from ..schemas.collection import RawMessageCreate


class CollectionService:
    """Service for storing raw messages from external sources."""

    def __init__(self, db: Session):
        self.db = db

    def create_raw_message(self, data: RawMessageCreate) -> RawMessage:
        msg = RawMessage(
            id=str(uuid4()),
            user_id=data.user_id,
            organization_id=data.organization_id,
            source=data.source,
            source_id=data.source_id,
            raw_content=data.raw_content,
            message_metadata=data.metadata,
            timestamp=data.timestamp,
            is_outgoing=data.is_outgoing,
            conversation_id=data.conversation_id,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_raw_message(self, message_id: str) -> RawMessage | None:
        return self.db.query(RawMessage).filter(RawMessage.id == message_id).first()
