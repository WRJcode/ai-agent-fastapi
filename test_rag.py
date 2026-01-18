# test_rag.py
from app.service.rag_service import rag_chat

if __name__ == "__main__":
    # ans = rag_chat("什么是 Java GC 算法？")
    ans = rag_chat("什么是 Java jvm？")
    print(ans)
