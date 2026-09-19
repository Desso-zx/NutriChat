from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services import retrieval, generation

router = APIRouter()

@router.get("/health")
def health_check():
    """Simple liveness check — does the server respond at all."""
    return {"status": "ok"}

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Full RAG flow: retrieve relevant chunks -> build prompt -> call the LLM
    -> return a grounded, cited answer.
    """
    try:
        retrieved_chunks = retrieval.retrieve(request.question)
        result = generation.generate_answer(request.question, retrieved_chunks)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return QueryResponse(answer=result["answer"], sources=result["sources"])