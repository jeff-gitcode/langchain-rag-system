class RetrieveDataQuery:
    def __init__(self, vector_db_repository):
        self.vector_db_repository = vector_db_repository

    def execute(self, criteria: dict):
        query = criteria.get("query")  # Extract the query string
        if not query:
            raise ValueError("Query field is required")
        return self.vector_db_repository.get_documents(query)