# app/prompt/rag.py
def build_rag_messages(question, contexts):
    context_text = "\n".join(contexts)
    return [
        {
            "role": "system",
            "content": "你是一个基于资料回答问题的助手，只能使用给定资料。"
        },
        {
            "role": "user",
            "content": f"""
资料：
{context_text}

问题：
{question}

请基于资料回答：
"""
        }
    ]
