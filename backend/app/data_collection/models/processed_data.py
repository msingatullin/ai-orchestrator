from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ProcessedMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    raw_message_id: UUID
    cleaned_text: str
    language: str
    sentiment_score: float
    emotion_tags: List[str] = Field(default_factory=list)
    message_type: str
    formality_level: float
    response_time_minutes: int | None = None
    contains_emoji: bool = False
    word_count: int = 0
    tokens: List[str] = Field(default_factory=list)
    lemmas: List[str] = Field(default_factory=list)
    conversation_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
