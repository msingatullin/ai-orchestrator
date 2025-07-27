from __future__ import annotations

import hashlib
from typing import List


class EmbeddingService:
    """Very simple embedding generator."""

    dimension = 10

    def encode_text(self, text: str) -> List[float]:
        """Encode text into a deterministic vector of floats."""
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # produce dimension floats by chunking digest
        ints = [b for b in digest[: self.dimension]]
        return [i / 255.0 for i in ints]
