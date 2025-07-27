from __future__ import annotations

import re
import secrets
from hashlib import sha256
from typing import Any

from cryptography.fernet import Fernet


class PrivacyService:
    """Simple privacy helper with symmetric encryption."""

    def __init__(self, key: bytes | None = None) -> None:
        self._key = key or Fernet.generate_key()
        self._fernet = Fernet(self._key)

    @property
    def key(self) -> bytes:
        return self._key

    def encrypt_message_content(self, content: str) -> str:
        return self._fernet.encrypt(content.encode()).decode()

    def decrypt_message_content(self, encrypted_content: str) -> str:
        return self._fernet.decrypt(encrypted_content.encode()).decode()

    def hash_conversation_id(self, original_id: str) -> str:
        return sha256(original_id.encode()).hexdigest()

    def remove_pii(self, text: str) -> str:
        email_re = r"[\w\.-]+@[\w\.-]+"
        phone_re = r"\+?\d[\d -]{7,}\d"
        text = re.sub(email_re, "[email]", text)
        text = re.sub(phone_re, "[phone]", text)
        return text
