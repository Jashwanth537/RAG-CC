import json
from typing import List
from langchain.schema import Document
import numpy as np
import os

def save_chunks_to_json(documents: List[Document], file_path: str):
    """Save a list of LangChain Document objects to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # ✅ Create directory if it doesn't exist
    json_docs = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_docs, f, ensure_ascii=False, indent=2)


def load_chunks_from_json(file_path: str) -> List[Document]:
    """Load a list of LangChain Document objects from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        json_docs = json.load(f)
    return [
        Document(page_content=d["page_content"], metadata=d["metadata"])
        for d in json_docs
    ]



def save_embeddings(arr, path):
    np.save(path, arr)

def load_embeddings(path):
    return np.load(path)