from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class RawMessageBase(BaseModel):
    user_id: str
    organization_id: Optional[str] = None
    source: str
    source_id: str
    raw_content: str
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="message_metadata")
    timestamp: datetime
    is_outgoing: bool = False
    conversation_id: Optional[str] = None


class RawMessageCreate(RawMessageBase):
    pass


class RawMessageRead(RawMessageBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
