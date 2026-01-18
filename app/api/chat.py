from fastapi import APIRouter
from app.service.chat_service import chat

router = APIRouter(tags=["chat"])

@router.post("/chat")
def chat_api(prompt: str):
    return {
        "response": chat(prompt)
    }
