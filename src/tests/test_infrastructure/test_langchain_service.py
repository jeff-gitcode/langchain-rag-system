from src.infrastructure.services.langchain_service import LangChainService
from unittest.mock import patch, MagicMock


def test_generate_response_with_ollama():
    # Mock the vector_db_repository if needed
    mock_vector_db_repository = MagicMock()

    # Initialize the LangChainService with the mocked repository
    service = LangChainService(mock_vector_db_repository)

    # Patch the requests.post method used in _langchain_generate
    with patch(
        "src.infrastructure.services.langchain_service.requests.post"
    ) as mock_post:
        # Mock the Ollama API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "response": "This is a test response from Ollama."
        }

        # Call the generate_response method
        response = service.generate_response("What is AI?")

        # Ensure the mock was called with the correct arguments
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": "What is AI?", "stream": False},
            headers={"Authorization": f"Bearer {service.api_key}"},
        )

        # Assert the response is as expected
        assert response == "This is a test response from Ollama."
