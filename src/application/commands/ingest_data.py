# FILE: src/application/commands/ingest_data.py
import uuid
from src.domain.entities.document import Document

class IngestDataCommand:
    def __init__(self, vector_db_repository):
        self.vector_db_repository = vector_db_repository

    def execute(self, data: dict):
        # Convert dict to Document instance
        document = Document(
            id=str(uuid.uuid4()),
            content=data["content"],
            metadata=data["metadata"]
        )
        self.vector_db_repository.add_document(document)