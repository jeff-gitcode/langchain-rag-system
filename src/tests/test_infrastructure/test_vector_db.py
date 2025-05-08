import os
import pytest
from src.infrastructure.database.vector_db import VectorDB
from src.domain.entities.document import Document

@pytest.fixture
def vector_db(tmp_path):
    db_path = tmp_path / "faiss_index"
    return VectorDB(db_path=str(db_path))

def test_add_document(vector_db):
    document = Document(id="1", content="Test content", metadata={"author": "John Doe"})
    vector_db.add_document(document)
    assert len(vector_db.documents) == 1

def test_get_documents(vector_db):
    document = Document(id="1", content="Test content", metadata={"author": "John Doe"})
    vector_db.add_document(document)
    results = vector_db.get_documents(query="Test content")
    assert len(results) > 0
    assert results[0].id == "1"