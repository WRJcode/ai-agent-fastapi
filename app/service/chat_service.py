from app.llm.llm_client import llm_client
from app.prompt.chat import build_chat_messages


def chat(prompt: str) -> str:
    messages = build_chat_messages(prompt)
    return llm_client.chat(messages)