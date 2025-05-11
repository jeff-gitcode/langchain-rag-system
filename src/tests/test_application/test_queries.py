from src.application.queries.retrieve_data import RetrieveDataQuery
from unittest.mock import Mock


def test_retrieve_data_query():
    mock_repository = Mock()
    mock_repository.get_documents.return_value = [
        {"id": "1", "content": "Test content"}
    ]
    query = RetrieveDataQuery(mock_repository)
    criteria = {"query": "Test content"}
    results = query.execute(criteria)
    mock_repository.get_documents.assert_called_once_with("Test content")
    assert len(results) > 0


def test_retrieve_data_query_no_results():
    mock_repository = Mock()
    mock_repository.get_documents.return_value = []  # Simulate no results
    query = RetrieveDataQuery(mock_repository)
    criteria = {"query": "Non-existent content"}
    results = query.execute(criteria)
    mock_repository.get_documents.assert_called_once_with("Non-existent content")
    assert len(results) == 0  # Assert that no results are returned


def test_retrieve_data_query_similarity_search():
    mock_repository = Mock()
    mock_repository.get_documents.return_value = [
        {"id": "1", "content": "Test content about AI"},
        {"id": "2", "content": "Another test content about machine learning"},
        {"id": "3", "content": "Unrelated content"},
    ]
    query = RetrieveDataQuery(mock_repository)
    criteria = {"query": "AI and machine learning"}
    results = query.execute(criteria)

    # Ensure the repository is called with the correct query
    mock_repository.get_documents.assert_called_once_with("AI and machine learning")

    # Assert that results are returned and sorted by relevance
    assert len(results) > 0
    assert (
        results[0]["id"] == "1"
    )  # Assuming the most relevant document is returned first
    assert results[1]["id"] == "2"  # Second most relevant document
    assert all(
        "AI" in doc["content"] or "machine learning" in doc["content"]
        for doc in results
    )
