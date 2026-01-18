class Synthesizer:
    def __init__(self, llm_client):
        self.llm = llm_client

    def summarize(self, user_input: str, results: str):
        messages = [
            {
                "role": "system",
                "content": "请基于执行结果，给用户一个清晰、直接的回答。"
            },
            {
                "role": "user",
                "content": f"""
问题：{user_input}

执行结果：
{results}
"""
            }
        ]

        resp = self.llm.chat(messages)
        return resp["content"]