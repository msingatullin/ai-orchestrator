from __future__ import annotations

from typing import List
import os

import logging

logger = logging.getLogger(__name__)


try:  # pragma: no cover - optional heavy dependency
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - if import fails
    SentenceTransformer = None

try:  # pragma: no cover - optional dependency
    import openai
except Exception:  # pragma: no cover - openai not installed
    openai = None


class EmbeddingService:
    """Generate embeddings using sentence-transformers or OpenAI."""

    def __init__(
        self,
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        openai_model: str = "text-embedding-ada-002",
    ) -> None:
        self.model = None
        self.dimension = None
        self.use_openai = False
        self.openai_model = openai_model

        if SentenceTransformer is not None:
            try:
                # avoid network fetches in restricted environments
                self.model = SentenceTransformer(model_name, local_files_only=True)
                self.dimension = self.model.get_sentence_embedding_dimension()
            except Exception as exc:  # pragma: no cover - handle init issues
                logger.warning("SentenceTransformer init failed: %s", exc)
                self.model = None

        if self.model is None and openai is not None:
            try:  # pragma: no cover - openai may not be configured
                if not getattr(openai, "api_key", None):
                    openai.api_key = os.environ.get("OPENAI_API_KEY")
                if not openai.api_key:
                    raise RuntimeError("OPENAI_API_KEY is not set")
                # dimension for default ada-002 model
                if self.openai_model == "text-embedding-ada-002":
                    self.dimension = 1536
                self.use_openai = True
            except Exception as exc:
                logger.warning("OpenAI init failed: %s", exc)

        if self.model is None and not self.use_openai:
            raise RuntimeError("No embedding backend available")

    def encode_text(self, text: str) -> List[float]:
        """Encode text into a vector using the selected backend."""
        if self.model is not None:
            vec = self.model.encode([text])[0]
            return vec.tolist() if hasattr(vec, "tolist") else list(vec)

        if self.use_openai:
            resp = openai.embeddings.create(model=self.openai_model, input=text)
            vec = resp.data[0].embedding
            if self.dimension is None:
                self.dimension = len(vec)
            return list(vec)

        raise RuntimeError("Embedding model not initialized")
