# app/rag/loader.py
from pathlib import Path

def load_documents(data_dir="data") -> list[str]:
    texts = []
    for file in Path(data_dir).glob("*.txt"):
        texts.append(file.read_text(encoding="utf-8"))
    return texts
