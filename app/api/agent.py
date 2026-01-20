from fastapi import APIRouter
from pydantic import BaseModel
from app.service.agent_service import AgentManager

router = APIRouter()
agent_manager = AgentManager(6000)


class ChatReq(BaseModel):
    prompt: str
    session_id: str


@router.post("/agent/chat")
def chat(req: ChatReq):
    agent = agent_manager.get_agent(req.session_id)
    answer = agent.chat(req.prompt)
    return {
        "session_id": req.session_id,
        "answer": answer
    }