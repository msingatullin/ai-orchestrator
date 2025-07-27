from __future__ import annotations

from typing import Dict, List, Tuple
from uuid import UUID

from ..utils.similarity import cosine_similarity


class VectorStoreService:
    """In-memory vector store for embeddings."""

    def __init__(self):
        self.collections: Dict[str, Dict[str, List[float]]] = {}
        self.metadata: Dict[str, Dict[str, Dict]] = {}

    def add_embedding(
        self,
        collection_name: str,
        embedding_id: str,
        vector: List[float],
        metadata: Dict | None = None,
    ) -> None:
        self.collections.setdefault(collection_name, {})[embedding_id] = vector
        self.metadata.setdefault(collection_name, {})[embedding_id] = metadata or {}

    def query(
        self,
        collection_name: str,
        query_vector: List[float],
        n_results: int = 5,
    ) -> List[Tuple[str, float]]:
        collection = self.collections.get(collection_name, {})
        results = []
        for eid, vec in collection.items():
            score = cosine_similarity(query_vector, vec)
            results.append((eid, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:n_results]
