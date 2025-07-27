from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from ..vector_db.services.search_service import SearchService
from ..vector_db.models.embeddings import MessageEmbedding
from ..data_collection.models.processed_data import ProcessedMessage

router = APIRouter()
search = SearchService()


@router.post("/index")
def index_message(data: ProcessedMessage, user_id: UUID):
    vector = search.embedder.encode_text(data.cleaned_text)
    embedding = MessageEmbedding(message_id=data.raw_message_id, user_id=user_id, vector=vector)
    search.add_message_embedding(embedding)
    return {"embedding_id": str(embedding.id)}


@router.get("/search")
def search_messages(user_id: UUID, query: str, limit: int = 5):
    results = search.search_messages(user_id, query, limit)
    return {"results": results}
