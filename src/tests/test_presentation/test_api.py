from src.presentation.api.main import app, mediator, vector_db
from src.domain.entities.document import Document  # Import the Document class
from fastapi.testclient import TestClient

client = TestClient(app)


def test_ingest_endpoint():
    response = client.post(
        "/ingest",
        json={
            "content": "The capybara is the largest rodent in the world.",
            "metadata": {"author": "John Doe", "category": "animals"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingested successfully"}


def test_retrieve_endpoint():
    # First, ingest a document
    client.post(
        "/ingest",
        json={"id": "1", "content": "Test content", "metadata": {"author": "John Doe"}},
    )
    # Then, retrieve it
    response = client.post("/retrieve", json={"query": "Test content"})
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0


def test_delete_endpoint():
    document_id = "test-document-id"
    document = Document(
        id=document_id, content="Test content", metadata={}
    )  # Create a Document object
    vector_db.add_document(document)  # Pass the Document object
    response = client.delete(f"/delete/{document_id}")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Document with ID {document_id} deleted successfully"
    }
