from src.application.commands.ingest_data import IngestDataCommand
from src.application.queries.retrieve_data import RetrieveDataQuery

class CLICommands:
    def __init__(self):
        self.ingest_command = IngestDataCommand()
        self.retrieve_query = RetrieveDataQuery()

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

    ingest_parser = subparsers.add_parser("ingest", help="Ingest data into the vector database")
    ingest_parser.add_argument("data", type=str, help="Data to ingest")

    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve data from the vector database")
    retrieve_parser.add_argument("criteria", type=str, help="Criteria for data retrieval")

    args = parser.parse_args()

    cli = CLICommands()

    if args.command == "ingest":
        cli.ingest_data(args.data)
    elif args.command == "retrieve":
        cli.retrieve_data(args.criteria)