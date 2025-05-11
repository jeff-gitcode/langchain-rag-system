from src.infrastructure.services.langchain_service import LangChainService
from unittest.mock import patch


def test_generate_response():
    service = LangChainService(None)  # Pass None for vector_db_repository if not needed
    with patch("openai.ChatCompletion.create") as mock_openai:
        mock_openai.return_value = {
            "choices": [{"message": {"content": "This is a test response."}}]
        }
        response = service.generate_response("What is AI?")
        assert response == "This is a test response."
