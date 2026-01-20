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

        messages = []

        # 1️⃣ system 指令
        messages.append({
            "role": "system",
            "content": "你是一个具备记忆能力的 AI Agent，请根据上下文进行规划。"
        })

        # 2️⃣ Short-term memory（直接 message 级注入）
        if short_ctx:
            messages.extend(short_ctx)

        # 3️⃣ Long-term memory（压缩成一条 system）
        if long_ctx:
            memory_text = "【相关历史记忆】\n" + "\n".join(
                f"- {item}" for item in long_ctx
            )
            messages.append({
                "role": "system",
                "content": memory_text
            })

        # 4️⃣ 当前用户输入（必须是 string）
        messages.append({
            "role": "user",
            "content": user_input
        })

        # 👉 Planner 现在只接收 messages
        plan = self.planner.plan(messages)

        result = self.executor.execute(plan)
        answer = self.synthesizer.summarize(user_input, result)

        # 5️⃣ 写回记忆
        self.short_memory.add_user_message(user_input)
        self.short_memory.add_assistant_message(answer)

        self.long_memory.add(
            f"用户问题：{user_input}；回答要点：{answer}"
        )

        return answer