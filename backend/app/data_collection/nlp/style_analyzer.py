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
                sentiment_distribution={},
                emotion_patterns={},
                dominant_sentiment=None,
                response_time_pattern={},
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

        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        emotion_counts: dict[str, int] = {}
        response_times: list[int] = []
        for m in msgs:
            if m.sentiment_score > 0.1:
                sentiments["positive"] += 1
            elif m.sentiment_score < -0.1:
                sentiments["negative"] += 1
            else:
                sentiments["neutral"] += 1

            for tag in getattr(m, "emotion_tags", []):
                emotion_counts[tag] = emotion_counts.get(tag, 0) + 1

            if m.response_time_minutes is not None:
                response_times.append(m.response_time_minutes)

        total = len(msgs)
        sentiment_distribution = {k: v / total for k, v in sentiments.items()}
        dominant_sentiment = max(sentiment_distribution, key=sentiment_distribution.get)
        emotion_patterns = {k: v / total for k, v in emotion_counts.items()}
        response_pattern = {}
        if response_times:
            response_pattern["average_minutes"] = sum(response_times) / len(response_times)

        return UserCommunicationStyle(
            user_id=user_id,
            source=source,
            avg_message_length=avg_len,
            formality_score=formality,
            emoji_usage_rate=emoji_rate,
            vocabulary_complexity=vocab_complexity,
            sentence_structure=structure,
            sentiment_distribution=sentiment_distribution,
            emotion_patterns=emotion_patterns,
            dominant_sentiment=dominant_sentiment,
            response_time_pattern=response_pattern,
        )
