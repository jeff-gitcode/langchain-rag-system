from src.application.commands.ingest_data import IngestDataCommand
from src.application.queries.retrieve_data import RetrieveDataQuery
from src.infrastructure.services.langchain_service import LangChainService
from src.infrastructure.database.vector_db import VectorDB


class CLICommands:
    def __init__(self):
        vector_db = VectorDB(db_path="./data/faiss_index")
        langchain_service = LangChainService(vector_db)
        self.ingest_command = IngestDataCommand(vector_db)
        self.retrieve_query = RetrieveDataQuery(
            vector_db, langchain_service
        )  # Pass langchain_service

    def ingest_data(self, data):
        result = self.ingest_command.execute(data)
        print(f"Data ingestion result: {result}")

    def retrieve_data(self, criteria):
        result = self.retrieve_query.execute(criteria)
        print(f"Retrieved data: {result}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CLI for RAG System")
    subparsers = parser.add_subparsers(dest="command")

    ingest_parser = subparsers.add_parser(
        "ingest", help="Ingest data into the vector database"
    )
    ingest_parser.add_argument("data", type=str, help="Data to ingest")

    retrieve_parser = subparsers.add_parser(
        "retrieve", help="Retrieve data from the vector database"
    )
    retrieve_parser.add_argument(
        "criteria", type=str, help="Criteria for data retrieval"
    )

    args = parser.parse_args()

    cli = CLICommands()

    if args.command == "ingest":
        cli.ingest_data(args.data)
    elif args.command == "retrieve":
        cli.retrieve_data(args.criteria)
