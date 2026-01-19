from typing import Dict
from app.agent.agent import Agent
from app.llm.llm_client import LLMClient


class AgentManager:
    """
    管理多 session 的 Agent 实例
    """
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._llm_client = LLMClient()

    def get_agent(self, session_id: str) -> Agent:
        if session_id not in self._agents:
            self._agents[session_id] = Agent(self._llm_client)
        return self._agents[session_id]