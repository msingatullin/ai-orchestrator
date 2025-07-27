from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.database import SessionLocal
from ..data_collection.parsers.telegram import TelegramParser
from ..data_collection.services.collection_service import CollectionService
from ..data_collection.schemas.collection import RawMessageRead

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


@router.get("/raw/{message_id}", response_model=RawMessageRead)
def get_raw_message(message_id: str, db: Session = Depends(get_db)):
    service = CollectionService(db)
    msg = service.get_raw_message(message_id)
    return msg
