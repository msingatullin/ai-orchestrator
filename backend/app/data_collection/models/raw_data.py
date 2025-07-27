from __future__ import annotations

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func

from ...models.base import Base


class RawMessage(Base):
    """Raw message collected from external sources."""

    __tablename__ = "raw_messages"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    source = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    raw_content = Column(String, nullable=False)
    message_metadata = Column("metadata", JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    is_outgoing = Column(Boolean, default=False)
    conversation_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
