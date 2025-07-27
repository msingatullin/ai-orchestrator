from __future__ import annotations

from typing import List
from uuid import UUID

from .embedding_service import EmbeddingService
from .vector_store import VectorStoreService
from ..models.embeddings import MessageEmbedding


class SearchService:
    """Simple semantic search over stored embeddings."""

    def __init__(self, store: VectorStoreService | None = None, embedder: EmbeddingService | None = None):
        self.store = store or VectorStoreService()
        self.embedder = embedder or EmbeddingService()

    def add_message_embedding(self, embedding: MessageEmbedding) -> None:
        self.store.add_embedding(
            collection_name=f"user_{embedding.user_id}_messages",
            embedding_id=str(embedding.id),
            vector=embedding.vector,
            metadata={"message_id": str(embedding.message_id)},
        )

    def search_messages(self, user_id: UUID, query: str, limit: int = 5) -> List[str]:
        qv = self.embedder.encode_text(query)
        results = self.store.query(
            collection_name=f"user_{user_id}_messages",
            query_vector=qv,
            n_results=limit,
        )
        return [r[0] for r in results]
