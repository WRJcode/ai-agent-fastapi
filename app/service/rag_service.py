# app/service/rag_service.py
from app.rag.loader import load_documents
from app.rag.splitter import split_text
from app.rag.embedding import embed_texts
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.prompt.rag import build_rag_messages
from app.llm.llm_client import llm_client

docs = load_documents()
chunks = []
for d in docs:
    chunks.extend(split_text(d))

vectors = embed_texts(chunks)
store = VectorStore(len(vectors[0]))
store.add(vectors, chunks)

retriever = Retriever(store)

def rag_chat(question: str) -> str:
    contexts = retriever.retrieve(question)
    messages = build_rag_messages(question, contexts)
    return llm_client.chat(messages)
