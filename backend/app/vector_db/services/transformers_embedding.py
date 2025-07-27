from __future__ import annotations

from typing import List

from sentence_transformers import SentenceTransformer


class TransformersEmbeddingService:
    """Embedding service backed by sentence-transformers."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2", **kwargs) -> None:
        self.model = SentenceTransformer(model_name, **kwargs)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode_text(self, text: str) -> List[float]:
        vec = self.model.encode([text])[0]
        return vec.tolist() if hasattr(vec, "tolist") else list(vec)
