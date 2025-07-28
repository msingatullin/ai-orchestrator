from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from ..services.digital_twin_service import DigitalTwinService
from ..models.digital_twin import DigitalTwin

router = APIRouter()
service = DigitalTwinService()


@router.post("/create", response_model=DigitalTwin)
async def create_twin(user_id: UUID, name: str) -> DigitalTwin:
    twin = await service.create_digital_twin(user_id, name)
    return twin


@router.post("/{twin_id}/generate")
async def generate(twin_id: UUID, query: str, rating: int | None = None) -> dict:
    if twin_id not in service.twins:
        raise HTTPException(status_code=404, detail="twin not found")
    text = await service.generate_response(twin_id, query, rating)
    return {"response": text}


@router.post("/{twin_id}/feedback")
async def feedback(twin_id: UUID, message: str, rating: int) -> dict:
    if twin_id not in service.twins:
        raise HTTPException(status_code=404, detail="twin not found")
    success = await service.feedback.record_feedback(twin_id, message, rating)
    return {"success": success}
