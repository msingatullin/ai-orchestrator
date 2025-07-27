from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UserCommunicationStyle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    source: str
    avg_message_length: float
    formality_score: float
    emoji_usage_rate: float
    response_time_pattern: Dict[str, float] = Field(default_factory=dict)
    vocabulary_complexity: float | None = None
    sentence_structure: Dict[str, float] = Field(default_factory=dict)
    common_phrases: List[str] = Field(default_factory=list)
    sentiment_distribution: Dict[str, float] = Field(default_factory=dict)
    emotion_patterns: Dict[str, float] = Field(default_factory=dict)
    active_hours: List[int] = Field(default_factory=list)
    conversation_starters: List[str] = Field(default_factory=list)
    typical_responses: Dict[str, str] = Field(default_factory=dict)
    dominant_sentiment: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
