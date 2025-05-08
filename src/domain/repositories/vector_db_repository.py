from abc import ABC, abstractmethod
from typing import List
from ..entities.document import Document

class VectorDBRepository(ABC):
    @abstractmethod
    def add_document(self, document: Document) -> None:
        pass

    @abstractmethod
    def get_documents(self, criteria: dict) -> List[Document]:
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        pass