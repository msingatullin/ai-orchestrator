from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from ..data_collection.nlp import NLPPipeline, StyleAnalyzer
from ..data_collection.models.processed_data import ProcessedMessage
from ..data_collection.models.user_style import UserCommunicationStyle

router = APIRouter()

pipeline = NLPPipeline()
analyzer = StyleAnalyzer()


class PipelineRequest(BaseModel):
    """Input schema for running the NLP pipeline on arbitrary text."""

    text: str
    conversation_id: str | None = None


class StyleRequest(BaseModel):
    """Input schema for computing a user's communication style."""

    messages: list[ProcessedMessage]
    user_id: str
    source: str


@router.post("/pipeline", response_model=ProcessedMessage)
def run_pipeline(data: PipelineRequest) -> ProcessedMessage:
    """Run the NLP pipeline for the provided text."""

    raw = SimpleNamespace(
        id=str(uuid4()),
        raw_content=data.text,
        conversation_id=data.conversation_id,
    )
    return pipeline.process(raw)


@router.post("/style", response_model=UserCommunicationStyle)
def analyze_style(data: StyleRequest) -> UserCommunicationStyle:
    """Generate a communication style profile from processed messages."""

    return analyzer.analyze(data.messages, data.user_id, data.source)
