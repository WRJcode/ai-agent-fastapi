from fastapi import APIRouter
from pydantic import BaseModel
from app.service.rag_service import rag_chat

router = APIRouter()

class RagRequest(BaseModel):
    question: str

@router.post("/rag/chat")
def rag_api(req: RagRequest):
    answer = rag_chat(req.question)
    return {"answer": answer}
