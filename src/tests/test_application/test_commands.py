from src.application.commands.ingest_data import IngestDataCommand
from src.domain.entities.document import Document
from unittest.mock import Mock

def test_ingest_data_command():
    mock_repository = Mock()
    command = IngestDataCommand(mock_repository)
    data = {"id": "1", "content": "Test content", "metadata": {"author": "John Doe"}}
    command.execute(data)
    mock_repository.add_document.assert_called_once()