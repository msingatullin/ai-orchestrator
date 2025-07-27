from __future__ import annotations

from uuid import UUID


class FeedbackHandler:
    """Placeholder for continual learning feedback."""

    async def record_feedback(self, twin_id: UUID, message: str, rating: int) -> bool:
        # In a real system this would update training data
        return True
