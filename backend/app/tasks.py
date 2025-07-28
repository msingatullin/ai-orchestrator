from __future__ import annotations

from uuid import UUID
import asyncio

from .celery_app import celery_app
from .digital_twin.services.digital_twin_service import DigitalTwinService

service = DigitalTwinService()

@celery_app.task
def generate_async(twin_id: str, query: str) -> str:
    """Generate a response from a digital twin in a Celery worker."""
    return asyncio.run(service.generate_response(UUID(twin_id), query))
