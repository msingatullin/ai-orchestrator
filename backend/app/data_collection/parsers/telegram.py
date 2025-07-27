from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..schemas.collection import RawMessageCreate


class TelegramParser:
    """Parse raw Telegram message payloads into internal schema objects."""

    @staticmethod
    def parse(payload: Dict[str, Any], user_id: str) -> RawMessageCreate:
        """Convert Telegram API message dict to RawMessageCreate."""
        return RawMessageCreate(
            user_id=user_id,
            source="telegram",
            source_id=str(payload.get("id")),
            raw_content=str(payload.get("text", "")),
            timestamp=datetime.fromtimestamp(payload.get("date", datetime.utcnow().timestamp())),
            is_outgoing=bool(payload.get("outgoing", False)),
            conversation_id=str(payload.get("chat_id", "")),
            metadata={k: v for k, v in payload.items() if k not in {"id", "text", "date", "outgoing", "chat_id"}},
        )
