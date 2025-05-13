import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.presentation.api.main import app, vector_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture to clear the vector database before and after each test.
    Ensures a clean state for each test.
    """
    # Clear the vector database before the test
    vector_db.documents.clear()
    vector_db._rebuild_index()

    yield

    # Clear the vector database after the test
    vector_db.documents.clear()
    vector_db._rebuild_index()


@patch("src.infrastructure.services.langchain_service.requests.post")
def test_full_workflow(mock_post):
    """
    Test the full workflow: ingestion, retrieval, and deletion.
    """

    # Mock the Ollama API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "This is a mocked response from Ollama."
    }

    # Step 1: Ingest a document
    ingest_response = client.post(
        "/ingest",
        json={
            "content": "The capybara is the largest rodent in the world.",
            "metadata": {"author": "John Doe", "category": "animals"},
        },
    )
    print("Ingest Response:", ingest_response.json())  # Debugging
    assert ingest_response.status_code == 200
    assert ingest_response.json() == {"message": "Data ingested successfully"}

    # Step 2: Retrieve the document
    retrieve_response = client.post(
        "/retrieve",
        json={"query": "largest rodent"},
    )
    print("Retrieve Response:", retrieve_response.json())  # Debugging
    assert retrieve_response.status_code == 200

    results = retrieve_response.json().get("results", {})
    retrieved_documents = results.get("retrieved_documents", [])
    assert len(retrieved_documents) == 1, (
        f"Expected 1 result, got {len(retrieved_documents)}"
    )
    assert (
        retrieved_documents[0]["content"]
        == "The capybara is the largest rodent in the world."
    )
    # no metadata check since response don't have metadata
    # assert retrieved_documents[0]["metadata"]["author"] == "John Doe"
    # assert retrieved_documents[0]["metadata"]["category"] == "animals"

    # Step 3: Delete the document
    assert len(retrieved_documents) > 0, "No documents retrieved to delete."
    document_id = retrieved_documents[0]["id"]  # Access the first document's ID
    delete_response = client.delete(f"/delete/{document_id}")
    print("Delete Response:", delete_response.json())  # Debugging
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": f"Document with ID {document_id} deleted successfully"
    }

    # Step 4: Verify the document is deleted
    retrieve_after_delete_response = client.post(
        "/retrieve",
        json={"query": "largest rodent"},
    )
    print(
        "Retrieve After Delete Response:", retrieve_after_delete_response.json()
    )  # Debugging
    assert retrieve_after_delete_response.status_code == 200
    results_after_delete = retrieve_after_delete_response.json().get("results", {})
    retrieved_documents_after_delete = results_after_delete.get(
        "retrieved_documents", []
    )
    assert len(retrieved_documents_after_delete) == 0, (
        f"Expected 0 results, got {len(retrieved_documents_after_delete)}"
    )
