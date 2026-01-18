# from app.agent.agent import run_agent

# def agent_chat(prompt: str) -> str:
#     return run_agent(prompt)

# app/service/agent_service.py

from app.agent.executor import AgentExecutor

executor = AgentExecutor()

def agent_chat(prompt: str) -> str:
    return executor.run(prompt)