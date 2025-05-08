from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.domain.entities.document import Document
from src.domain.repositories.vector_db_repository import VectorDBRepository
import os
from dotenv import load_dotenv
import json

load_dotenv()

class VectorDB(VectorDBRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.metadata_path = f"{db_path}_metadata.json"
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained model

        # Get the dimensionality of the embedding model
        embedding_dim = len(self.embedding_model.encode("test"))

        # Initialize FAISS index with the correct dimensionality
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []  # To store metadata and content

        # Load FAISS index if it exists
        if os.path.exists(self.db_path):
            self.index = faiss.read_index(self.db_path)

        # Load metadata if it exists
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                self.documents = json.load(f)

    def add_document(self, document: Document) -> None:
        # Convert document content to vector
        vector = self.embedding_model.encode(document.content)
        vector = np.array([vector]).astype('float32')

        # Add vector to FAISS index
        self.index.add(vector)

        # Store document metadata
        self.documents.append(document.__dict__)

        # Save FAISS index and metadata to disk
        faiss.write_index(self.index, self.db_path)
        with open(self.metadata_path, "w") as f:
            json.dump(self.documents, f)

    def get_documents(self, query: str, top_k: int = 5) -> List[Document]:
        # Convert query to vector
        query_vector = self.embedding_model.encode(query)
        query_vector = np.array([query_vector]).astype('float32')

        # Perform similarity search
        distances, indices = self.index.search(query_vector, top_k)

        # Retrieve corresponding documents
        results = [Document(**self.documents[i]) for i in indices[0] if i < len(self.documents)]
        return results
    
    def delete_document(self, document_id: str) -> None:
        # Remove the document with the given ID
        self.documents = [doc for doc in self.documents if doc["id"] != document_id]
        with open(self.metadata_path, "w") as f:
            json.dump(self.documents, f)