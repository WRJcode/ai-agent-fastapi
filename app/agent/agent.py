from app.agent.planner import Planner
from app.agent.plan_executor import PlanExecutor
from app.agent.synthesizer import Synthesizer
from app.agent.memory import ShortTermMemory, LongTermMemory


class Agent:
    def __init__(self, llm_client):
        self.planner = Planner(llm_client)
        self.executor = PlanExecutor()
        self.synthesizer = Synthesizer(llm_client)

        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

    def chat(self, user_input: str) -> str:
        short_ctx = self.short_memory.get_context()
        long_ctx = self.long_memory.search(user_input)

        memory_prompt = self._build_memory_prompt(short_ctx, long_ctx)

        plan = self.planner.plan(user_input, memory_prompt)
        result = self.executor.execute(plan)
        answer = self.synthesizer.summarize(user_input, result)

        self.short_memory.add_user_message(user_input)
        self.short_memory.add_assistant_message(answer)

        self.long_memory.add(
            f"用户问题：{user_input}；回答要点：{answer}"
        )

        return answer

    def _build_memory_prompt(self, short_ctx, long_ctx):
        text = ""

        if short_ctx:
            text += "【最近对话】\n"
            for m in short_ctx:
                text += f"{m['role']}: {m['content']}\n"

        if long_ctx:
            text += "\n【相关历史记忆】\n"
            for item in long_ctx:
                text += f"- {item}\n"

        return text