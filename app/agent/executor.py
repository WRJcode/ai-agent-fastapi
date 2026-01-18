# app/agent/executor.py

import json
from app.agent.tools import TOOL_MAP
from app.llm.llm_client import llm_client
from app.agent.dsml import extract_query_from_dsml

class AgentExecutor:
    def __init__(self, max_steps: int = 5):
        self.max_steps = max_steps

    def run(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": "你是一个具备工具调用能力的 AI Agent"},
            {"role": "user", "content": user_input}
        ]

        for step in range(self.max_steps):
            response = llm_client.chat(
                messages=messages,
                tools=self._tool_schema()
            )

            # ========== 情况 1：标准 tool_calls ==========
            if response.get("tool_calls"):
                self._handle_tool_calls(response, messages)
                continue

            content = response.get("content", "")

            # ========== 情况 2：DeepSeek DSML ==========
            if "<｜DSML｜function_calls>" in content:
                self._handle_dsml(content, messages)
                continue

            # ========== 情况 3：最终答案 ==========
            return content

        raise RuntimeError("Agent exceeded max steps without final answer")

    # ---------- 工具处理 ----------

    def _handle_tool_calls(self, response, messages):
        tool_call = response["tool_calls"][0]
        name = tool_call["function"]["name"]
        args = json.loads(tool_call["function"]["arguments"])

        result = TOOL_MAP[name](**args)

        messages.append({
            "role": "assistant",
            "tool_calls": response["tool_calls"]
        })

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": str(result)
        })

    def _handle_dsml(self, content: str, messages):
        query = extract_query_from_dsml(content)
        result = TOOL_MAP["search_knowledge_base"](query)

        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "tool",
            "content": str(result)
        })

    # ---------- Tool Schema ----------

    def _tool_schema(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "从知识库中检索信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "检索关键词"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
