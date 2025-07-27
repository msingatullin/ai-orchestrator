from __future__ import annotations

from typing import List
import hashlib


try:  # pragma: no cover - optional heavy dependency
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - if import fails fall back to hash
    SentenceTransformer = None


class EmbeddingService:
    """Generate embeddings using a Transformer model with a hash fallback."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2") -> None:
        self.model = None
        self.dimension = 10
        if SentenceTransformer is not None:
            try:
                # avoid network fetches in restricted environments
                self.model = SentenceTransformer(model_name, local_files_only=True)
                self.dimension = self.model.get_sentence_embedding_dimension()
            except Exception:
                self.model = None

    def encode_text(self, text: str) -> List[float]:
        """Encode text into a vector using the selected backend."""
        if self.model is not None:
            vec = self.model.encode([text])[0]
            return vec.tolist() if hasattr(vec, "tolist") else list(vec)
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        ints = [b for b in digest[: self.dimension]]
        return [i / 255.0 for i in ints]
