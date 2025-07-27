from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ConversationContext(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    conversation_id: str
    source: str
    participant_count: int
    start_time: datetime
    end_time: datetime
    message_count: int
    topic_keywords: List[str] = Field(default_factory=list)
    conversation_type: str
    average_response_time: float | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
