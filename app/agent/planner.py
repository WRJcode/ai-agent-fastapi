class Planner:
    def __init__(self, llm_client):
        self.llm = llm_client

    def plan(self, messages):
        """
        messages: List[{"role": str, "content": str}]
        """

        print("\n[Planner] messages sent to LLM:")
        for i, m in enumerate(messages):
            print(f"[{i}] {m['role']}: {m['content']}\n")

        # ⚠️ 关键点：不再二次包装 messages
        resp = self.llm.chat(messages)

        return resp["content"]