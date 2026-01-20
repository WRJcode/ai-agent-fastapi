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
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []

    def add(self, text: str):
        emb = self.model.encode([text])
        self.index.add(np.array(emb).astype("float32"))
        self.texts.append(text)
        print(f"[LongTermMemory] add text, total={len(self.texts)}")

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.texts:
            print("[LongTermMemory] search skipped (empty)")
            return []

        emb = self.model.encode([query])
        _, idx = self.index.search(
            np.array(emb).astype("float32"),
            top_k
        )

        results = [self.texts[i] for i in idx[0] if i < len(self.texts)]
        print(f"[LongTermMemory] search query='{query}', hit={len(results)}")
        return results