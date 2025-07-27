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
                vocabulary_complexity=0,
                sentence_structure={},
            )

        avg_len = mean(m.word_count for m in msgs)
        formality = mean(m.formality_level for m in msgs)
        emoji_rate = sum(1 for m in msgs if m.contains_emoji) / len(msgs)

        all_lemmas = [lemma for m in msgs for lemma in getattr(m, "lemmas", m.tokens)]
        vocab_complexity = (
            len(set(all_lemmas)) / len(all_lemmas) if all_lemmas else 0.0
        )

        short = sum(1 for m in msgs if m.word_count < 5) / len(msgs)
        medium = sum(1 for m in msgs if 5 <= m.word_count <= 15) / len(msgs)
        long = sum(1 for m in msgs if m.word_count > 15) / len(msgs)
        structure = {"short": short, "medium": medium, "long": long}

        return UserCommunicationStyle(
            user_id=user_id,
            source=source,
            avg_message_length=avg_len,
            formality_score=formality,
            emoji_usage_rate=emoji_rate,
            vocabulary_complexity=vocab_complexity,
            sentence_structure=structure,
        )
