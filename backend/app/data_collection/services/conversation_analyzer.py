from __future__ import annotations

from statistics import mean
from typing import Iterable

from ..models import ConversationContext, ProcessedMessage


class ConversationAnalyzer:
    """Build conversation context summaries."""

    def build_context(
        self,
        messages: Iterable[ProcessedMessage],
        user_id: str,
        conversation_id: str,
        source: str,
    ) -> ConversationContext:
        msgs = sorted(messages, key=lambda m: m.created_at)
        if not msgs:
            raise ValueError("no messages")
        start = msgs[0].created_at
        end = msgs[-1].created_at
        avg_resp = (
            mean(m.response_time_minutes for m in msgs if m.response_time_minutes is not None)
            if any(m.response_time_minutes is not None for m in msgs)
            else None
        )
        return ConversationContext(
            user_id=user_id,
            conversation_id=conversation_id,
            source=source,
            participant_count=1,
            start_time=start,
            end_time=end,
            message_count=len(msgs),
            topic_keywords=[],
            conversation_type="chat",
            average_response_time=avg_resp,
            summary=None,
        )
