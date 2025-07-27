from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..schemas.collection import RawMessageCreate


class WhatsAppParser:
    """Parser for WhatsApp message payloads."""

    @staticmethod
    def parse(payload: Dict[str, Any], user_id: str) -> RawMessageCreate:
        ts_val = payload.get("timestamp")
        if isinstance(ts_val, (int, float)):
            ts = datetime.fromtimestamp(ts_val)
        else:
            ts = datetime.utcnow()
        return RawMessageCreate(
            user_id=user_id,
            source="whatsapp",
            source_id=str(payload.get("id")),
            raw_content=str(payload.get("text", "")),
            timestamp=ts,
            is_outgoing=bool(payload.get("from_me", False)),
            conversation_id=str(payload.get("chat_id", "")),
            metadata={k: v for k, v in payload.items() if k not in {"id", "text", "timestamp", "from_me", "chat_id"}},
        )
