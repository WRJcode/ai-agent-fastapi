from typing import List, Dict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class ShortTermMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.messages: List[Dict[str, str]] = []
        print(f"[ShortTermMemory] init max_turns={self.max_turns}")

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        print(f"[ShortTermMemory] add user message, total={len(self.messages)}")
        self._trim()

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        print(f"[ShortTermMemory] add assistant message, total={len(self.messages)}")
        self._trim()

    def get_context(self) -> List[Dict[str, str]]:
        print(f"[ShortTermMemory] get_context size={len(self.messages)}")
        return list(self.messages)

    def _trim(self):
        max_messages = self.max_turns * 2
        if len(self.messages) > max_messages:
            before = len(self.messages)
            self.messages = self.messages[-max_messages:]
            after = len(self.messages)
            print(f"[ShortTermMemory] trim messages: {before} -> {after}")


class LongTermMemory:
    def __init__(self, dim: int = 384):
        print("[LongTermMemory] init")
        self.keys: List[str] = []      # 用来 embedding & search
        self.values: List[str] = []   # 真正存的知识
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        print("[LongTermMemory] duplicate_threshold=0.92 (cosine similarity)")

    def _cosine_sim(self, a: np.ndarray, b: np.ndarray) -> float:
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        if a_norm == 0 or b_norm == 0:
            return 0.0
        return float(np.dot(a, b) / (a_norm * b_norm))

    def add(self, question: str, summary: str):
        emb = self.model.encode([question])
        emb = np.array(emb).astype("float32")

        if self.keys:
            D, I = self.index.search(emb, 1)
            sim = 1 - D[0][0]  # L2 → similarity
            print(f"[LongTermMemory] check duplicate sim={sim:.4f}")

            if sim > 0.92:
                print(
                    "[LongTermMemory] skip write "
                    "(semantic duplicate question)"
                )
                return

        self.index.add(emb)
        self.keys.append(question)
        self.values.append(summary)

        print(
            f"[LongTermMemory] write new fact memory "
            f"(total={len(self.values)})"
        )

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.keys:
            print("[LongTermMemory] search skipped (empty)")
            return []

        emb = self.model.encode([query])
        emb = np.array(emb).astype("float32")

        _, idx = self.index.search(emb, top_k)

        results = [self.values[i] for i in idx[0] if i < len(self.values)]
        print(f"[LongTermMemory] search hit={len(results)}")
        return results