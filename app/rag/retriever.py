# app/rag/retriever.py
from app.rag.embedding import embed_texts

class Retriever:
    def __init__(self, store):
        self.store = store

    def retrieve(self, query, top_k=3):
        vector = embed_texts([query])[0]
        return self.store.search(vector, top_k)
