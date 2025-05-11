import os
import pytest
from src.infrastructure.database.vector_db import VectorDB
from src.domain.entities.document import Document


@pytest.fixture
def vector_db():
    # Ensure the test FAISS index and metadata are cleared before each test
    db_path = "./data/faiss_index_test"
    metadata_path = f"{db_path}_metadata.json"

    yield VectorDB(db_path=db_path)

    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)

    # Return a fresh instance of VectorDB
    # Create a fresh instance of VectorDB
    vector_db = VectorDB(db_path=db_path)

    # Rebuild the index to ensure synchronization
    vector_db._rebuild_index()

    return vector_db


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

    results = vector_db.get_documents(query="AI content", top_k=2)
    assert len(results) == 2
    assert results[0].content == "AI content"
    assert results[1].content == "Machine learning content"


def test_vector_db_better_similarity_search(vector_db):
    vector_db.add_document(
        Document(id="1", content="AI content", metadata={"category": "technology"})
    )
    vector_db.add_document(
        Document(
            id="2",
            content="Machine learning content",
            metadata={"category": "technology"},
        )
    )
    vector_db.add_document(
        Document(
            id="3",
            content="Unrelated content about cooking",
            metadata={"category": "cooking"},
        )
    )
    vector_db.add_document(
        Document(
            id="4",
            content="Deep learning advancements",
            metadata={"category": "technology"},
        )
    )
    vector_db.add_document(
        Document(id="5", content="AI and robotics", metadata={"category": "technology"})
    )

    query = "AI and machine learning"
    results = vector_db.get_documents(query=query, top_k=3)

    # Print results for debugging
    print("Results:")
    for result in results:
        print(
            f"ID: {result.id}, Content: {result.content}, Metadata: {result.metadata}"
        )

    # Assertions
    assert len(results) == 3  # Ensure the correct number of results is returned
    assert results[0].content in ["AI content", "AI and robotics"]
    assert results[1].content in [
        "Machine learning content",
        "Deep learning advancements",
    ]
    assert results[2].content in ["AI content", "AI and robotics"]
