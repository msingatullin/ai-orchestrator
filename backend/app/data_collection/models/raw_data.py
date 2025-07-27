from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RawMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    source: str
    source_id: str
    raw_content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime
    is_outgoing: bool
    conversation_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
