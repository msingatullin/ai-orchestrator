from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DigitalTwin(BaseModel):
    """Simplified Digital Twin model."""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    name: str
    status: str = "training"
    base_model: str = "gpt-3.5-turbo"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    communication_style: Optional[dict] = None


class PersonalityProfile(BaseModel):
    """Minimal personality profile placeholder."""

    id: UUID = Field(default_factory=uuid4)
    digital_twin_id: UUID
    description: str
