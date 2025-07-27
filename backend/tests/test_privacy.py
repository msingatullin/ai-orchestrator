from uuid import uuid4

import pytest

from backend.app.data_collection.services import PrivacyService, DataRetentionService


@pytest.mark.asyncio
async def test_privacy_encryption_roundtrip():
    service = PrivacyService()
    text = "secret message"
    encrypted = service.encrypt_message_content(text)
    assert encrypted != text
    decrypted = service.decrypt_message_content(encrypted)
    assert decrypted == text


@pytest.mark.asyncio
async def test_data_retention_schedule():
    retention = DataRetentionService()
    future = await retention.schedule_data_deletion(uuid4(), 7)
    assert future
