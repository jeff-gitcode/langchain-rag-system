from fastapi.testclient import TestClient
from src.presentation.api.main import app

client = TestClient(app)

def test_ingest_endpoint():
    response = client.post("/ingest", json={
        "id": "1",
        "content": "Test content",
        "metadata": {"author": "John Doe"}
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingested successfully"}

def test_retrieve_endpoint():
    # First, ingest a document
    client.post("/ingest", json={
        "id": "1",
        "content": "Test content",
        "metadata": {"author": "John Doe"}
    })
    # Then, retrieve it
    response = client.get("/retrieve", json={"query": "Test content"})
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0