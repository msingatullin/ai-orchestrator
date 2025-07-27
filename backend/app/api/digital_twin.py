from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..digital_twin.services.digital_twin_service import DigitalTwinService
from ..digital_twin.models.digital_twin import DigitalTwin

router = APIRouter()
service = DigitalTwinService()


class TwinCreateRequest(BaseModel):
    """Request schema for creating a digital twin."""

    user_id: UUID
    name: str


class GenerateRequest(BaseModel):
    """Request schema for generating a response from a digital twin."""

    query: str


@router.post("/create", response_model=DigitalTwin)
async def create_twin(user_id: UUID, name: str) -> DigitalTwin:
    """Create a new digital twin for the given user."""

    twin = await service.create_digital_twin(user_id, name)
    return twin


@router.post("/{twin_id}/generate")
async def generate(twin_id: UUID, query: str) -> dict:
    """Generate an LLM-based response from the specified digital twin."""

    if twin_id not in service.twins:
        raise HTTPException(status_code=404, detail="twin not found")
    text = await service.generate_response(twin_id, query)
    return {"response": text}
