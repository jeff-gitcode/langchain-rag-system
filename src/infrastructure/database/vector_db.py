import os
import json
import faiss
import numpy as np
from typing import List
from src.domain.repositories.vector_db_repository import VectorDBRepository
from src.domain.entities.document import Document  # Adjust the import path as needed
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class VectorDB(VectorDBRepository):
    def __init__(self, db_path: str, metadata_path=None, embedding_model=None):
        self.db_path = db_path  # Path for FAISS index
        self.metadata_path = (
            metadata_path or f"{db_path}_metadata.json"
        )  # Path for metadata
        self.embedding_model = embedding_model or SentenceTransformer(
            "all-MiniLM-L6-v2"
        )  # Pre-trained model

        # Get the dimensionality of the embedding model
        test_vector = self.embedding_model.encode("test")  # Generate a test embedding
        embedding_dim = len(test_vector)

        # Initialize FAISS index with the correct dimensionality
        self.index = faiss.IndexFlatL2(embedding_dim)

        # Load FAISS index if it exists
        if os.path.exists(self.db_path):
            try:
                self.index = faiss.read_index(self.db_path)
                if self.index.d != embedding_dim:
                    raise ValueError(
                        f"FAISS index dimensionality ({self.index.d}) does not match embedding model dimensionality ({embedding_dim})."
                    )
            except RuntimeError as e:
                print(
                    f"Warning: Failed to load FAISS index from {self.db_path}. Initializing a new index. Error: {e}"
                )
                self.index = faiss.IndexFlatL2(embedding_dim)

        # Load metadata if it exists
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, "r") as f:
                    self.documents = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(
                    f"Warning: Failed to load metadata from {self.metadata_path}. Initializing empty metadata. Error: {e}"
                )
                self.documents = []
        else:
            self.documents = []

    def add_document(self, document: Document):
        # Convert document content to vector
        vector = self.embedding_model.encode(document.content)
        vector = vector / np.linalg.norm(vector)  # Normalize the vector
        vector = np.array([vector]).astype("float32")

        # Add vector to FAISS index
        self.index.add(vector)

        # Save metadata
        self.documents.append(
            {
                "id": document.id,
                "content": document.content,
                "metadata": document.metadata,
            }
        )
        with open(self.metadata_path, "w") as f:
            json.dump(self.documents, f)

        # Save FAISS index
        faiss.write_index(self.index, self.db_path)

    def get_documents(self, query: str, top_k: int = 5) -> List[Document]:
        # Convert query to vector
        query_vector = self.embedding_model.encode(query)
        query_vector = query_vector / np.linalg.norm(
            query_vector
        )  # Normalize the vector
        query_vector = np.array([query_vector]).astype("float32")

        # Perform similarity search
        distances, indices = self.index.search(query_vector, top_k)
        print("Distances:", distances)
        print("Indices:", indices)

        # Retrieve documents, ensuring indices are within bounds
        valid_documents = []
        for i in indices[0]:
            if 0 <= i < len(self.documents):  # Check if index is valid
                valid_documents.append(Document(**self.documents[i]))
            else:
                print(f"Warning: Index {i} is out of range for documents list.")

        return valid_documents

    def delete_document(self, document_id: str) -> None:
        # Remove the document with the given ID
        self.documents = [doc for doc in self.documents if doc["id"] != document_id]
        with open(self.metadata_path, "w") as f:
            json.dump(self.documents, f)

        # Rebuild the FAISS index to ensure synchronization
        self._rebuild_index()

    def _rebuild_index(self):
        """Rebuild the FAISS index from the current documents."""
        self.index.reset()  # Clear the FAISS index
        for doc in self.documents:
            vector = self.embedding_model.encode(doc["content"])
            vector = np.array([vector]).astype("float32")
            self.index.add(vector)
        faiss.write_index(self.index, self.db_path)
