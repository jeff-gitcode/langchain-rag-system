import pytest
from unittest.mock import Mock
from src.domain.entities.document import Document
from src.application.queries.retrieve_data import RetrieveDataQuery


@pytest.fixture
def mock_vector_db_repository():
    return Mock()


@pytest.fixture
def mock_langchain_service():
    return Mock()


@pytest.fixture
def retrieve_data_query(mock_vector_db_repository, mock_langchain_service):
    return RetrieveDataQuery(mock_vector_db_repository, mock_langchain_service)


def test_execute_with_valid_query(
    retrieve_data_query, mock_vector_db_repository, mock_langchain_service
):
    # Mock the vector database to return relevant documents
    mock_vector_db_repository.get_documents.return_value = [
        Document(id="1", content="AI is transforming industries.", metadata={}),
        Document(id="2", content="Machine learning is a subset of AI.", metadata={}),
    ]

    # Mock the LangChain service to generate a response
    mock_langchain_service.generate_response.return_value = (
        "AI is widely used in various industries."
    )

    # Define the query criteria
    criteria = {"query": "How is AI used in industries?"}

    # Execute the query
    result = retrieve_data_query.execute(criteria)

    # Assertions
    mock_vector_db_repository.get_documents.assert_called_once_with(
        "How is AI used in industries?"
    )
    mock_langchain_service.generate_response.assert_called_once_with(
        "Query: How is AI used in industries?\nContext: AI is transforming industries. Machine learning is a subset of AI."
    )

    assert result["query"] == "How is AI used in industries?"
    assert len(result["retrieved_documents"]) == 2
    assert result["retrieved_documents"][0]["id"] == "1"
    assert result["retrieved_documents"][1]["id"] == "2"
    assert result["generated_response"] == "AI is widely used in various industries."


def test_execute_with_no_query(retrieve_data_query):
    # Define criteria without a query
    criteria = {}

    # Execute the query and expect a ValueError
    with pytest.raises(ValueError, match="Query field is required"):
        retrieve_data_query.execute(criteria)


def test_execute_with_empty_documents(
    retrieve_data_query, mock_vector_db_repository, mock_langchain_service
):
    # Declare an empty array for Document objects
    mock_vector_db_repository.get_documents.return_value = []

    # Mock the LangChain service to generate a response
    mock_langchain_service.generate_response.return_value = (
        "No relevant documents found."
    )

    # Define the query criteria
    criteria = {"query": "What is AI?"}

    # Execute the query
    result = retrieve_data_query.execute(criteria)

    # Assertions
    mock_vector_db_repository.get_documents.assert_called_once_with("What is AI?")
    mock_langchain_service.generate_response.assert_not_called()  # No documents, so no call to generate_response

    assert result["query"] == "What is AI?"
    assert len(result["retrieved_documents"]) == 0
    assert result["generated_response"] == "No relevant documents found."


def test_execute_with_large_context(
    retrieve_data_query, mock_vector_db_repository, mock_langchain_service
):
    # Mock the vector database to return many documents
    mock_vector_db_repository.get_documents.return_value = [
        Document(id=str(i), content=f"Document {i} content.", metadata={})
        for i in range(1, 6)
    ]

    # Mock the LangChain service to generate a response
    mock_langchain_service.generate_response.return_value = (
        "Generated response for a large context."
    )

    # Define the query criteria
    criteria = {"query": "Explain the documents."}

    # Execute the query
    result = retrieve_data_query.execute(criteria)

    # Assertions
    mock_vector_db_repository.get_documents.assert_called_once_with(
        "Explain the documents."
    )
    mock_langchain_service.generate_response.assert_called_once_with(
        "Query: Explain the documents.\nContext: Document 1 content. Document 2 content. Document 3 content. Document 4 content. Document 5 content."
    )

    assert result["query"] == "Explain the documents."
    assert len(result["retrieved_documents"]) == 5
    assert result["generated_response"] == "Generated response for a large context."
