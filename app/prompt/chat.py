from app.prompt.system import BASE_SYSTEM_PROMPT


def build_chat_messages(user_prompt: str):
    return [
        {"role": "system", "content": BASE_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]