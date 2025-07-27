from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class RawMessageBase(BaseModel):
    user_id: str
    organization_id: Optional[str] = None
    source: str
    source_id: str
    raw_content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime
    is_outgoing: bool = False
    conversation_id: Optional[str] = None


class RawMessageCreate(RawMessageBase):
    pass


class RawMessageRead(RawMessageBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
        fields = {"metadata": "message_metadata"}
