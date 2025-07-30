# 📊 RAG Chatbot Evaluation Guide

This directory contains tools to evaluate your RAG chatbot's performance across multiple dimensions.

## 🎯 Evaluation Metrics

### 1. **Retrieval Quality**
- **Precision@K**: How many retrieved documents are actually relevant
- **Similarity Scores**: Cosine similarity between query and retrieved chunks
- **Source Coverage**: Whether the right documents are being found

### 2. **Generation Quality**
- **Answer Relevance**: How well the answer addresses the question
- **Faithfulness**: How well the answer sticks to the retrieved context
- **LLM Judge Scores**: AI-based evaluation of relevance, accuracy, completeness, clarity

### 3. **Performance Metrics**
- **Response Time**: How fast the system responds
- **Consistency**: How consistent answers are across multiple runs

## 🔧 Quick Start

### Option 1: Simple Evaluation (Recommended for beginners)

```bash
# Activate your environment
source ragproj/bin/activate

# Run simple evaluation with manual feedback
python evaluation/simple_eval.py
```

This will:
- Test 4 sample questions
- Show detailed results for each
- Ask you to manually rate the answers
- Provide a summary

### Option 2: Comprehensive Evaluation

```bash
# Run full automated evaluation
python evaluation/run_evaluation.py
```

This will:
- Test all 8 questions from `test_questions.json`
- Generate automated metrics
- Use LLM-as-a-judge evaluation
- Save detailed results to `evaluation_results.json`

## 📁 Files Overview

```
evaluation/
├── test_questions.json      # Test questions with expected answers
├── rag_evaluator.py        # Main evaluation framework
├── run_evaluation.py       # Automated evaluation runner
├── simple_eval.py          # Interactive evaluation tool
└── README.md              # This guide
```

## 🧪 Test Questions Categories

1. **Fees** - Annual fees, joining fees, charges
2. **Rewards** - Cashback rates, reward points, benefits
3. **Eligibility** - Income requirements, age criteria
4. **Policies** - Payment deadlines, penalties, terms
5. **Benefits** - Special offers, waivers, perks
6. **Comparison** - Multi-card comparisons
7. **Usage** - How to use cards, activation process

## 📈 Understanding Results

### Sample Output:
```
📊 RAG EVALUATION SUMMARY
============================================================
📝 Total Questions: 8
⏱️  Avg Response Time: 2.34s

🔍 RETRIEVAL METRICS:
  • Precision@3: 0.750      # 75% of retrieved docs are relevant
  • Avg Similarity: 0.682   # Good semantic matching

🤖 GENERATION METRICS:
  • Answer Relevance: 0.834  # Answers are quite relevant
  • Faithfulness: 0.756     # Answers stick to context well

👨‍⚖️ LLM JUDGE SCORES (1-5):
  • Relevance: 4.2/5        # High relevance
  • Accuracy: 3.8/5         # Good accuracy
  • Completeness: 3.5/5     # Room for improvement
  • Clarity: 4.1/5          # Clear answers
```

## 🎯 Interpreting Scores

### Retrieval Metrics
- **Precision@3 > 0.7**: Good retrieval
- **Similarity > 0.6**: Strong semantic matching
- **< 0.5**: Consider improving embeddings or chunking

### Generation Metrics  
- **Answer Relevance > 0.8**: Excellent
- **0.6-0.8**: Good
- **< 0.6**: Needs improvement

### LLM Judge Scores
- **4-5**: Excellent quality
- **3-4**: Good quality
- **2-3**: Acceptable, room for improvement
- **< 2**: Needs significant improvement

## 🔧 Customizing Evaluation

### Add Your Own Questions

Edit `test_questions.json`:

```json
{
  "id": "q9",
  "question": "Your custom question here",
  "expected_info": "What info should be found",
  "relevant_sources": ["expected_pdf_sources.pdf"],
  "difficulty": "easy|medium|hard",
  "category": "your_category"
}
```

### Modify Evaluation Criteria

In `rag_evaluator.py`, you can:
- Adjust similarity thresholds
- Change LLM judge prompts
- Add new evaluation metrics
- Modify scoring algorithms

## 🚀 Best Practices

1. **Run Regular Evaluations**: Test after any changes to your system
2. **Use Multiple Metrics**: Don't rely on just one evaluation method
3. **Manual Review**: Always manually check a few answers
4. **Track Over Time**: Keep evaluation results to track improvements
5. **Category Analysis**: Look at performance by question category

## 🔍 Troubleshooting

### Low Retrieval Scores
- Check your document chunking strategy
- Verify embeddings are working correctly
- Consider adjusting similarity thresholds

### Low Generation Scores
- Review your prompt template
- Check if retrieved context is relevant
- Consider using a different LLM

### Slow Response Times
- Optimize your embedding model
- Check Pinecone performance
- Consider caching strategies

## 📊 Advanced Analysis

For deeper insights, check the detailed JSON results:

```python
import json
with open('evaluation/evaluation_results.json', 'r') as f:
    results = json.load(f)

# Analyze by category
for result in results['detailed_results']:
    category = result['category']
    score = result['answer_relevance']
    print(f"{category}: {score:.3f}")
```

## 🎯 Next Steps

1. **Baseline**: Run initial evaluation to establish baseline
2. **Iterate**: Make improvements to your RAG system
3. **Re-evaluate**: Test again to measure improvements
4. **Deploy**: Use evaluation to validate before production

Happy evaluating! 🚀 