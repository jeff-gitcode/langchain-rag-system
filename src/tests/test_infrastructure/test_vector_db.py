import pytest
from src.infrastructure.database.vector_db import VectorDB
from src.domain.entities.document import Document


@pytest.fixture
def vector_db():
    # Create a fresh instance of VectorDB for each test
    return VectorDB(db_path="./data/faiss_index_test")


def test_add_document(vector_db):
    document = Document(id="1", content="Test content", metadata={"author": "John Doe"})
    vector_db.add_document(document)
    assert len(vector_db.documents) == 1


def test_get_documents(vector_db):
    document = Document(id="1", content="Test content", metadata={"author": "John Doe"})
    vector_db.add_document(document)
    results = vector_db.get_documents(query="Test content", top_k=1)
    assert len(results) > 0
    assert results[0].id == "1"


def test_vector_db_similarity_search(vector_db):
    vector_db.add_document(Document(id="1", content="AI content", metadata={}))
    vector_db.add_document(
        Document(id="2", content="Machine learning content", metadata={})
    )
    vector_db.add_document(Document(id="3", content="Unrelated content", metadata={}))

    results = vector_db.get_documents(query="AI", top_k=2)
    assert len(results) == 2
    assert results[0].content == "AI content"
    assert results[1].content == "Machine learning content"
