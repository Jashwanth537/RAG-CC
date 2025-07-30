# 💳 Credit Card QA – RAG System

A **RAG** pipeline for answering queries about Indian credit cards.

---

## Current Status

- ✅ Extract and chunk data 
- ✅ Embeddings using Hugging Face's `all-MiniLM-L6-v2`
- ✅ **Pinecone** for semantic search
- ✅ **Groq LLM** for response generation

---

## 📁 Project Structure

```
.
├── app/
│   └── main.py          # FastAPI app
│
├── utils/
│   ├── chunking.py             # PDF reading and text chunking
│   ├── embedding.py            # Embeddings & LLM response generation
│   └── io.py                   # Saving/loading utilities
├── data/
│   └── pdfs/                   # raw PDFs
├── saved/
│   ├── chunks.pkl              # Saved chunks
│   └── embeddings.npy          # Saved embeddings
│
├── prepare_data.py            # chunk → embed → save
└── requirements.txt
```

---

## 🧠 Stack
- **LLM:** Groq (Llama 3) - Free tier available
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB:** Pinecone
- **API:** FastAPI (planned)
- **Tools:** LangChain

---

## 🔧 Quick Start

```bash
# Setup environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys:
# - PINECONE_API_KEY=your_pinecone_key
# - GROQ_API_KEY=your_groq_key

# Start the RAG system
python -m app.main 
```

### 🔑 API Keys Setup

1. **Pinecone**: Sign up at [pinecone.io](https://pinecone.io) (free tier available)
2. **Groq**: Sign up at [groq.com](https://groq.com) (generous free tier)

---

## 🛣️ Roadmap

- ✅ Add LLM for response generation (Groq/Llama 3)
- Add Fast API backend
- Integrate Chain-of-Thought reasoning
- Streamlit UI
- Docker + CI/CD pipeline
- Logging & observability for MLOps

---
