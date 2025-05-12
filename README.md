# 💳 Credit Card QA – RAG System

A **RAG** pipeline for answering queries about Indian credit cards.

---

## Current Status

- Extract and chunk data 
- Embeddings using Hugging Face’s `all-MiniLM-L6-v2`
- **Pinecone** for semantic search
- 

---

## 📁 Project Structure

```
.
├── app/
│   ├── loader.py        # PDF extraction
│   ├── splitter.py      # Text chunking
│   ├── embedder.py      # Hugging Face embeddings
│   ├── retriever.py     # Pinecone search
│   └── main.py          # FastAPI app
├── data/pdfs/           # Source documents
├── pinecone_setup.py
├── Dockerfile
└── requirements.txt
```

---

## 🧠 Stack
- **LLM:** LLama 3
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB:** Pinecone
- **API:** FastAPI
- **Tools:** LangChain

---

## 🔧 Quick Start

```bash
# Setup environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Start API server
python -m app.main 
```

---

## 🛣️ Roadmap

- Add Fast API backend
- Add LLM for response generation (Mistral, LLaMA 3)
- Integrate Chain-of-Thought reasoning
- Streamlit UI
- Docker + CI/CD pipeline
- Logging & observability for MLOps

---
