from openai import OpenAI
from app.core.config import settings


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )

    def chat(self, messages):
        resp = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return {
            "content": resp.choices[0].message.content
        }