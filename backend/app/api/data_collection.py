from __future__ import annotations

from fastapi import APIRouter, Depends
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
