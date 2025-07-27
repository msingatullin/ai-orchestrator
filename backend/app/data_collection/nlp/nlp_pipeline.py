from __future__ import annotations

import re
import string
from .sentiment_analyzer import SentimentAnalyzer
from ..models import ProcessedMessage, RawMessage


class NLPPipeline:
    """Simple NLP processing pipeline for raw messages."""

    emoji_re = re.compile(r"[\U0001F600-\U0001F64F]")

    def __init__(self) -> None:
        self.sentiment = SentimentAnalyzer()

    def clean_text(self, text: str) -> str:
        text = text.strip()
        return text.translate(str.maketrans("", "", string.punctuation))

    def detect_language(self, text: str) -> str:
        if re.search(r"[а-яА-Я]", text):
            return "ru"
        return "en"

    def formality_level(self, text: str) -> float:
        tokens = text.lower().split()
        polite = {"please", "thank", "thanks"}
        if not tokens:
            return 0.0
        count = sum(1 for t in tokens if t in polite)
        return count / len(tokens)

    def process(self, message: RawMessage) -> ProcessedMessage:
        cleaned = self.clean_text(message.raw_content)
        language = self.detect_language(cleaned)
        sentiment = self.sentiment.analyze(cleaned)
        contains_emoji = bool(self.emoji_re.search(message.raw_content))
        word_count = len(cleaned.split())
        formality = self.formality_level(cleaned)
        return ProcessedMessage(
            raw_message_id=message.id,
            cleaned_text=cleaned,
            language=language,
            sentiment_score=sentiment,
            emotion_tags=[],
            message_type="text",
            formality_level=formality,
            response_time_minutes=None,
            contains_emoji=contains_emoji,
            word_count=word_count,
        )
