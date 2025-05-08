from fastapi import FastAPI
from pydantic import BaseModel
from src.infrastructure.database.vector_db import VectorDB
from src.application.mediator import AppMediator
import os
from dotenv import load_dotenv

class IngestRequest(BaseModel):
    id: str
    content: str
    metadata: dict
    
# Define request model
class RetrieveRequest(BaseModel):
    query: str
        
# Initialize dependencies
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'default-secret')
vector_db = VectorDB(db_path=VECTOR_DB_PATH)
mediator = AppMediator(vector_db)

app = FastAPI()

@app.post("/ingest")
def ingest_data(data: IngestRequest):
    mediator.send("ingest_data", data.__dict__)
    return {"message": "Data ingested successfully"}

@app.get("/retrieve")
def retrieve_data(criteria: RetrieveRequest):
    results = mediator.send("retrieve_data", criteria.__dict__)
    return {"results": results}