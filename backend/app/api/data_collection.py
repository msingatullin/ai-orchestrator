from __future__ import annotations

from fastapi import APIRouter, Depends
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..config.database import SessionLocal
from ..data_collection.parsers import (
    TelegramParser,
    EmailParser,
    WhatsAppParser,
)
from ..data_collection.services.collection_service import CollectionService
from ..data_collection.schemas.collection import RawMessageRead
from ..data_collection.nlp import NLPPipeline
from ..data_collection.models.processed_data import ProcessedMessage

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/telegram", response_model=RawMessageRead)
def ingest_telegram_message(payload: dict, user_id: str, db: Session = Depends(get_db)):
    parser = TelegramParser()
    data = parser.parse(payload, user_id)
    service = CollectionService(db)
    msg = service.create_raw_message(data)
    return msg


@router.post("/email", response_model=RawMessageRead)
def ingest_email_message(payload: dict, user_id: str, db: Session = Depends(get_db)):
    parser = EmailParser()
    data = parser.parse(payload, user_id)
    service = CollectionService(db)
    msg = service.create_raw_message(data)
    return msg


@router.post("/whatsapp", response_model=RawMessageRead)
def ingest_whatsapp_message(payload: dict, user_id: str, db: Session = Depends(get_db)):
    parser = WhatsAppParser()
    data = parser.parse(payload, user_id)
    service = CollectionService(db)
    msg = service.create_raw_message(data)
    return msg


@router.post("/telegram/import", response_model=list[RawMessageRead])
def import_telegram_messages(payloads: list[dict], user_id: str, db: Session = Depends(get_db)):
    parser = TelegramParser()
    service = CollectionService(db)
    results = [service.create_raw_message(parser.parse(p, user_id)) for p in payloads]
    return results


@router.post("/email/import", response_model=list[RawMessageRead])
def import_email_messages(payloads: list[dict], user_id: str, db: Session = Depends(get_db)):
    parser = EmailParser()
    service = CollectionService(db)
    results = [service.create_raw_message(parser.parse(p, user_id)) for p in payloads]
    return results


@router.get("/raw/{message_id}", response_model=RawMessageRead)
def get_raw_message(message_id: str, db: Session = Depends(get_db)):
    service = CollectionService(db)
    msg = service.get_raw_message(message_id)
    return msg


@router.post("/process/{message_id}", response_model=ProcessedMessage)
def process_message(message_id: str, db: Session = Depends(get_db)):
    service = CollectionService(db)
    msg = service.get_raw_message(message_id)
    pipeline = NLPPipeline()
    return pipeline.process(msg)


@router.get("/data/export")
async def export_user_data(user_id: str):
    from ..data_collection.services import DataRetentionService

    service = DataRetentionService()
    return await service.export_user_data(UUID(user_id))


@router.delete("/data/delete")
async def delete_user_data(user_id: str):
    from ..data_collection.services import DataRetentionService

    service = DataRetentionService()
    return await service.delete_user_data(UUID(user_id))


@router.post("/data/anonymize")
async def anonymize_old(user_id: str, days: int = 30):
    from ..data_collection.services import DataRetentionService
    from datetime import datetime, timedelta

    service = DataRetentionService()
    cutoff = datetime.utcnow() - timedelta(days=days)
    return await service.anonymize_old_data(cutoff)
