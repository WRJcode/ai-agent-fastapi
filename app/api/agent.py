from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import Agent
from app.llm.llm_client import LLMClient

router = APIRouter()

agent = Agent(LLMClient())


class ChatReq(BaseModel):
    prompt: str


@router.post("/agent/chat")
def chat(req: ChatReq):
    answer = agent.chat(req.prompt)
    return {"answer": answer}