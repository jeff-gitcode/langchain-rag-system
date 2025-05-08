from src.application.queries.retrieve_data import RetrieveDataQuery
from unittest.mock import Mock

def test_retrieve_data_query():
    mock_repository = Mock()
    mock_repository.get_documents.return_value = [{"id": "1", "content": "Test content"}]
    query = RetrieveDataQuery(mock_repository)
    criteria = {"query": "Test content"}
    results = query.execute(criteria)
    mock_repository.get_documents.assert_called_once_with("Test content")
    assert len(results) > 0