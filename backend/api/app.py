from fastapi import FastAPI
from pydantic import BaseModel
from backend.models.rag_runner import answer_query

app = FastAPI()

class QueryIn(BaseModel):
    question: str
    top_k: int = 4

class QueryOut(BaseModel):
    answer: str

@app.post("/query", response_model=QueryOut)
def query(q: QueryIn):
    try:
        resp = answer_query(q.question, top_k=q.top_k)
    except Exception as e:
        resp =f"[ERROR] {str(e)}"
    return {"answer": resp}

