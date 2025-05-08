# FILE: src/domain/entities/document.py
class Document:
    def __init__(self, id: str, content: str, metadata: dict):
        self.id = id
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"Document(id={self.id}, content={self.content}, metadata={self.metadata})"