# FILE: src/application/mediator.py
from abc import ABC, abstractmethod
from src.application.commands.ingest_data import IngestDataCommand
from src.application.queries.retrieve_data import RetrieveDataQuery
from src.infrastructure.services.langchain_service import LangChainService


class Mediator(ABC):
    @abstractmethod
    def send(self, request_type: str, data: dict):
        pass


class AppMediator(Mediator):
    def __init__(self, vector_db_repository):
        self.vector_db_repository = vector_db_repository
        self.langchain_service = LangChainService(
            vector_db_repository
        )  # Initialize LangChainService
        self.handlers = {
            "ingest_data": IngestDataCommand(vector_db_repository),
            "retrieve_data": RetrieveDataQuery(
                vector_db_repository, self.langchain_service
            ),
        }

    def send(self, request_type: str, data: dict):
        handler = self.handlers.get(request_type)
        if not handler:
            raise ValueError(f"No handler found for request type: {request_type}")
        return handler.execute(data)
