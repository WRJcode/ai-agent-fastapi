import time
from typing import Dict, Tuple
from app.agent.agent import Agent
from app.llm.llm_client import LLMClient


class AgentManager:
    """
    管理多 session 的 Agent 实例（支持 TTL）
    """

    def __init__(self, ttl_seconds: int = 600):
        self._agents: Dict[str, Tuple[Agent, float]] = {}
        self._llm_client = LLMClient()
        self._ttl = ttl_seconds

    def get_agent(self, session_id: str) -> Agent:
        now = time.time()

        # 先清理过期 session
        self._cleanup_expired(now)

        if session_id not in self._agents:
            print(f"[AgentManager] create new agent for session: {session_id}")
            agent = Agent(self._llm_client)
            self._agents[session_id] = (agent, now)
        else:
            agent, _ = self._agents[session_id]
            # 更新最后访问时间
            self._agents[session_id] = (agent, now)
            print(f"[AgentManager] reuse agent for session: {session_id}")

        return self._agents[session_id][0]

    def _cleanup_expired(self, now: float):
        expired_sessions = [
            session_id
            for session_id, (_, last_ts) in self._agents.items()
            if now - last_ts > self._ttl
        ]

        for session_id in expired_sessions:
            print(f"[AgentManager] session expired: {session_id}")
            del self._agents[session_id]