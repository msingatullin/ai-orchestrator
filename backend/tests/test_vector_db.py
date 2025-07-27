import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from uuid import uuid4

from backend.app.vector_db import EmbeddingService, SearchService, MessageEmbedding
from backend.app.data_collection.models.processed_data import ProcessedMessage


def test_embedding_creation():
    service = EmbeddingService()
    pm = ProcessedMessage(
        raw_message_id=uuid4(),
        cleaned_text="hello world",
        language="en",
        sentiment_score=0.5,
        message_type="text",
        formality_level=0.5,
    )
    vector = service.encode_text(pm.cleaned_text)
    assert len(vector) == service.dimension
    assert service.dimension in (384, 1536)


def test_vector_storage_and_search():
    embedder = EmbeddingService()
    search = SearchService()
    user_id = uuid4()

    msg1 = ProcessedMessage(
        raw_message_id=uuid4(),
        cleaned_text="hello world",
        language="en",
        sentiment_score=0.5,
        message_type="text",
        formality_level=0.5,
    )

    emb1 = MessageEmbedding(message_id=msg1.id, user_id=user_id, vector=embedder.encode_text(msg1.cleaned_text))
    search.add_message_embedding(emb1)

    results = search.search_messages(user_id, "hello world", limit=1)
    assert results[0] == str(emb1.id)
