from __future__ import annotations

from statistics import mean
from typing import Iterable

from ..models import ProcessedMessage, UserCommunicationStyle


class StyleAnalyzer:
    """Analyze a user's communication style from processed messages."""

    def analyze(
        self, messages: Iterable[ProcessedMessage], user_id: str, source: str
    ) -> UserCommunicationStyle:
        msgs = list(messages)
        if not msgs:
            return UserCommunicationStyle(
                user_id=user_id,
                source=source,
                avg_message_length=0,
                formality_score=0,
                emoji_usage_rate=0,
            )

        avg_len = mean(m.word_count for m in msgs)
        formality = mean(m.formality_level for m in msgs)
        emoji_rate = sum(1 for m in msgs if m.contains_emoji) / len(msgs)

        return UserCommunicationStyle(
            user_id=user_id,
            source=source,
            avg_message_length=avg_len,
            formality_score=formality,
            emoji_usage_rate=emoji_rate,
        )
