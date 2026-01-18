from app.service.rag_service import rag_chat
import re

def search_knowledge_base(query: str) -> str:
    """
    从知识库中检索信息
    """
    return rag_chat(query)


def calculator(expression: str) -> str:
    """
    简单计算器
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

def extract_query_from_dsml(text: str) -> str:
    match = re.search(r'parameter name="query".*?>(.*?)<', text)
    return match.group(1) if match else ""

def is_intermediate(response: dict) -> bool:
    if response.get("tool_calls"):
        return True

    content = response.get("content", "")
    if "<｜DSML｜function_calls>" in content:
        return True

    return False

# app/agent/tools.py

def search_knowledge_base(query: str) -> str:
    # 你已有的 RAG 检索逻辑
    return f"【知识库结果】与「{query}」相关的内容..."

TOOL_MAP = {
    "search_knowledge_base": search_knowledge_base
}