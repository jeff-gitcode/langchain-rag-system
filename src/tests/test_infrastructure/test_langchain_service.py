from src.infrastructure.services.langchain_service import LangChainService
from unittest.mock import Mock

def test_generate_response():
    mock_repository = Mock()
    service = LangChainService(mock_repository)
    response = service.generate_response("What is LangChain?")
    assert "LangChain" in response