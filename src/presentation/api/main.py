from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.infrastructure.database.vector_db import VectorDB
from src.application.mediator import AppMediator
import os
from dotenv import load_dotenv


class IngestRequest(BaseModel):
    content: str
    metadata: dict


# Define request model
class RetrieveRequest(BaseModel):
    query: str


# Initialize dependencies
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "default-secret")
vector_db = VectorDB(db_path=VECTOR_DB_PATH)
mediator = AppMediator(vector_db)

app = FastAPI()


@app.post("/ingest")
def ingest_data(data: IngestRequest):
    mediator.send("ingest_data", data.__dict__)
    return {"message": "Data ingested successfully"}


@app.post("/retrieve")
def retrieve_data(criteria: RetrieveRequest):
    results = mediator.send("retrieve_data", criteria.__dict__)
    return {"results": results}


@app.delete("/delete/{document_id}")
def delete_document(document_id: str):
    try:
        vector_db.delete_document(document_id)
        return {"message": f"Document with ID {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
