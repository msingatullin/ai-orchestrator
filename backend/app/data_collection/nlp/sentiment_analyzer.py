from __future__ import annotations

import string

POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "happy",
    "love",
    "awesome",
    "nice",
}

NEGATIVE_WORDS = {
    "bad",
    "terrible",
    "sad",
    "hate",
    "awful",
    "horrible",
}

class SentimentAnalyzer:
    """Naive rule based sentiment analyzer."""

    def analyze(self, text: str) -> float:
        words = [w.strip(string.punctuation).lower() for w in text.split()]
        pos = sum(1 for w in words if w in POSITIVE_WORDS)
        neg = sum(1 for w in words if w in NEGATIVE_WORDS)
        total = pos + neg
        if total == 0:
            return 0.0
        return (pos - neg) / total
