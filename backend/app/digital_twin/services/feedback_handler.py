from __future__ import annotations

from uuid import UUID
from typing import Dict, List, Tuple


class FeedbackHandler:
    """In-memory feedback storage for Digital Twins."""

    def __init__(self) -> None:
        self._store: Dict[UUID, List[Tuple[str, int]]] = {}

    async def record_feedback(self, twin_id: UUID, message: str, rating: int) -> bool:
        """Record feedback for a digital twin."""
        self._store.setdefault(twin_id, []).append((message, rating))
        return True

    def get_feedback_history(self, twin_id: UUID) -> List[Tuple[str, int]]:
        """Retrieve feedback history for a digital twin."""
        return list(self._store.get(twin_id, []))
