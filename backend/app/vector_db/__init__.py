from .services.embedding_service import EmbeddingService
from .services.search_service import SearchService
from .services.vector_store import VectorStoreService
from .models.embeddings import MessageEmbedding

try:  # pragma: no cover - optional heavy dependency
    from .services.transformers_embedding import TransformersEmbeddingService
except Exception:  # pragma: no cover - fallback when dependency missing
    TransformersEmbeddingService = None

__all__ = [
    "EmbeddingService",
    "SearchService",
    "VectorStoreService",
    "MessageEmbedding",
    "TransformersEmbeddingService",
]
