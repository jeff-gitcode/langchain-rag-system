from src.domain.entities.document import Document

def test_document_initialization():
    document = Document(id="1", content="Test content", metadata={"author": "John Doe"})
    assert document.id == "1"
    assert document.content == "Test content"
    assert document.metadata == {"author": "John Doe"}