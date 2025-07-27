from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MessageEmbedding(BaseModel):
    """Simplified message embedding model."""

    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    user_id: UUID
    vector: List[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)
