# 💳 Credit Card QA – RAG System

A **RAG** pipeline for answering queries about Indian credit cards.

---

## Current Status

- ✅ Extract and chunk data 
- ✅ Embeddings using Hugging Face's `all-MiniLM-L6-v2`
- ✅ **Pinecone** for semantic search
- ✅ **Groq LLM** for response generation
- ✅ **Evaluation framework** with automated metrics

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
├── evaluation/
│   ├── rag_evaluator.py        # Comprehensive evaluation framework
│   ├── simple_eval.py          # Interactive evaluation tool
│   ├── run_evaluation.py       # Automated evaluation runner
│   ├── test_questions.json     # Test dataset
│   └── README.md              # Evaluation guide
│
├── prepare_data.py            # chunk → embed → save
└── requirements.txt
```

---

## 🧠 Stack
- **LLM:** Groq (Llama 3) - llama3-8b-8192
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

# Test the system (optional but recommended)
python evaluation/simple_eval.py
```

### 🔑 API Keys Setup

1. **Pinecone**: Sign up at [pinecone.io](https://pinecone.io) (free tier available)
2. **Groq**: Sign up at [groq.com](https://groq.com) (generous free tier)

---

## 📊 Evaluation & Testing

The system includes a comprehensive evaluation framework to measure RAG performance:

### Quick Evaluation (Interactive)
```bash
# Test with 4 sample questions + manual rating
python evaluation/simple_eval.py
```

### Full Automated Evaluation
```bash
# Run all 8 test questions with automated metrics
python evaluation/run_evaluation.py
```

### Evaluation Metrics
- **Retrieval Quality**: Precision@K, similarity scores
- **Generation Quality**: Answer relevance, faithfulness to context  
- **LLM-as-a-Judge**: Automated scoring for relevance, accuracy, completeness
- **Performance**: Response time, consistency

### Sample Results
```
📊 RAG EVALUATION SUMMARY
============================================================
📝 Total Questions: 8
⏱️  Avg Response Time: 2.75s

🔍 RETRIEVAL METRICS:
  • Precision@3: 0.750      # 75% retrieved docs relevant
  • Avg Similarity: 0.682   # Good semantic matching

🤖 GENERATION METRICS:
  • Answer Relevance: 0.834  # High relevance
  • Faithfulness: 0.756     # Sticks to context well

👨‍⚖️ LLM JUDGE SCORES (1-5):
  • Relevance: 4.2/5        # Excellent
  • Accuracy: 3.8/5         # Good  
  • Completeness: 3.5/5     # Room for improvement
  • Clarity: 4.1/5          # Clear answers
```

📁 **Detailed evaluation guide**: `evaluation/README.md`

---

## 🛣️ Roadmap

- ✅ Add LLM for response generation (Groq/Llama 3)
- ✅ Comprehensive evaluation framework with automated metrics
- 🔄 Add Fast API backend
- 🔄 Integrate Chain-of-Thought reasoning  
- 🔄 Streamlit UI
- 🔄 Docker + CI/CD pipeline
- 🔄 Logging & observability for MLOps

## 🎯 Performance Benchmarks

| Metric | Current Score | Target | Status |
|--------|---------------|--------|--------|
| Response Time | ~2.75s | <2.0s | 🟡 Good |
| Answer Relevance | 4.0/5 | >4.2/5 | 🟡 Good |
| Retrieval Precision | 0.75 | >0.8 | 🟡 Good |
| Faithfulness | 0.76 | >0.8 | 🟡 Good |

## 🔧 Development Workflow

1. **Make Changes** to RAG system (prompts, embeddings, chunking, etc.)
2. **Run Evaluation** to measure impact:
   ```bash
   python evaluation/simple_eval.py  # Quick test
   # or
   python evaluation/run_evaluation.py  # Full evaluation
   ```
3. **Compare Results** with baseline metrics
4. **Iterate** based on evaluation insights
5. **Deploy** once performance targets are met

---
