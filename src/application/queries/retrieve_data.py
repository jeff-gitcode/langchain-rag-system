from typing import List
from src.infrastructure.services.langchain_service import LangChainService
from src.domain.entities.document import Document


class RetrieveDataQuery:
    def __init__(self, vector_db_repository, langchain_service: LangChainService):
        self.vector_db_repository = vector_db_repository
        self.langchain_service = langchain_service

    def execute(self, criteria: dict):
        query = criteria.get("query")  # Extract the query string
        if not query:
            raise ValueError("Query field is required")

        # Step 1: Retrieve relevant documents
        documents: List[Document] = self.vector_db_repository.get_documents(query)

        # Convert Document objects to dictionaries
        documents = [{"id": doc.id, "content": doc.content} for doc in documents]

        # print the retrieved documents for debugging
        print(f"Retrieved documents: {documents}")
        if not documents:
            return {
                "query": query,
                "retrieved_documents": [],
                "generated_response": "No relevant documents found.",
            }

        # Step 2: Generate a response using the retrieved documents
        context = " ".join(
            [doc["content"] for doc in documents]
        )  # Combine document content
        response = self.langchain_service.generate_response(
            f"Query: {query}\nContext: {context}"
        )

        # Step 3: Return the response and the retrieved documents
        return {
            "query": query,
            "retrieved_documents": documents,
            "generated_response": response,
        }
