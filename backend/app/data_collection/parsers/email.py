from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..schemas.collection import RawMessageCreate


class EmailParser:
    """Parser for email message payloads."""

    @staticmethod
    def parse(payload: Dict[str, Any], user_id: str) -> RawMessageCreate:
        date = payload.get("date")
        if isinstance(date, str):
            try:
                ts = datetime.fromisoformat(date)
            except ValueError:
                ts = datetime.utcnow()
        else:
            ts = datetime.utcnow()
        return RawMessageCreate(
            user_id=user_id,
            source="email",
            source_id=str(payload.get("id")),
            raw_content=str(payload.get("body", "")),
            timestamp=ts,
            is_outgoing=bool(payload.get("outgoing", False)),
            conversation_id=str(payload.get("thread_id", "")),
            metadata={k: v for k, v in payload.items() if k not in {"id", "body", "date", "outgoing", "thread_id"}},
        )
