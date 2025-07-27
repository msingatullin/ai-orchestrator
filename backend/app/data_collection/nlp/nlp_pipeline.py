from __future__ import annotations

import re
import string
from typing import List

from .sentiment_analyzer import SentimentAnalyzer
from ..models import ProcessedMessage, RawMessage


class NLPPipeline:
    """Simple NLP processing pipeline for raw messages."""

    emoji_re = re.compile(r"[\U0001F600-\U0001F64F]")

    emotion_map = {
        "joy": {"happy", "glad", "love", "awesome", "great"},
        "sadness": {"sad", "unhappy", "down", "depressed"},
        "anger": {"angry", "mad", "furious", "rage"},
        "fear": {"scared", "afraid", "fearful"},
        "surprise": {"surprised", "wow"},
    }

    def __init__(self) -> None:
        self.sentiment = SentimentAnalyzer()

    def tokenize(self, text: str) -> List[str]:
        """Split text into word tokens."""
        return re.findall(r"\b\w+\b", text.lower())

    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """Naive lemmatization using simple suffix stripping."""
        lemmas = []
        for tok in tokens:
            lemma = tok
            for suf in ("ing", "ed", "s"):
                if lemma.endswith(suf) and len(lemma) > len(suf) + 2:
                    lemma = lemma[: -len(suf)]
                    break
            lemmas.append(lemma)
        return lemmas

    def extract_emotions(self, lemmas: List[str]) -> List[str]:
        tags: set[str] = set()
        for lemma in lemmas:
            for tag, words in self.emotion_map.items():
                if lemma in words:
                    tags.add(tag)
        return sorted(tags)

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

    def process(
        self, message: RawMessage, previous_message: RawMessage | None = None
    ) -> ProcessedMessage:
        """Process a raw message into structured data."""
        cleaned = self.clean_text(message.raw_content)
        language = self.detect_language(cleaned)

        tokens = self.tokenize(cleaned)
        lemmas = self.lemmatize_tokens(tokens)

        sentiment = self.sentiment.analyze(cleaned)
        emotions = self.extract_emotions(lemmas)

        contains_emoji = bool(self.emoji_re.search(message.raw_content))
        word_count = len(tokens)
        formality = self.formality_level(cleaned)

        response_time = None
        if previous_message and previous_message.timestamp:
            delta = message.timestamp - previous_message.timestamp
            response_time = int(delta.total_seconds() // 60)

        return ProcessedMessage(
            raw_message_id=message.id,
            cleaned_text=cleaned,
            language=language,
            sentiment_score=sentiment,
            emotion_tags=emotions,
            message_type="text",
            formality_level=formality,
            response_time_minutes=response_time,
            contains_emoji=contains_emoji,
            word_count=word_count,
            tokens=tokens,
            lemmas=lemmas,
            conversation_id=message.conversation_id,
        )
