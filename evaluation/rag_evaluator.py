"""
RAG Chatbot Evaluation Framework
Evaluates retrieval quality, generation quality, and end-to-end performance
"""

import json
import numpy as np
from typing import List, Dict, Tuple
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.append('..')
from utils.embedding import query, generate_response, embedder, groq_client
import time

class RAGEvaluator:
    def __init__(self):
        self.embedder = embedder
        self.results = []
        
    def load_test_questions(self, filepath: str) -> List[Dict]:
        """Load test questions from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['test_questions']
    
    def evaluate_retrieval(self, query_text: str, retrieved_docs: List, relevant_sources: List[str]) -> Dict:
        """
        Evaluate retrieval quality
        - Precision@K: How many retrieved docs are relevant
        - Recall: How many relevant docs were retrieved
        - Average similarity score
        """
        retrieved_sources = [doc.metadata.get('source', '') for doc in retrieved_docs]
        
        # Precision@K (how many retrieved are actually relevant)
        relevant_retrieved = sum(1 for source in retrieved_sources 
                               if any(rel_source in source for rel_source in relevant_sources))
        precision_at_k = relevant_retrieved / len(retrieved_docs) if retrieved_docs else 0
        
        # Calculate average similarity scores
        scores = [doc.score for doc in retrieved_docs] if hasattr(retrieved_docs[0], 'score') else [0.5] * len(retrieved_docs)
        avg_similarity = np.mean(scores) if scores else 0
        
        return {
            'precision_at_k': precision_at_k,
            'avg_similarity_score': avg_similarity,
            'retrieved_sources': retrieved_sources,
            'num_retrieved': len(retrieved_docs)
        }
    
    def evaluate_answer_relevance(self, question: str, answer: str) -> float:
        """
        Evaluate how relevant the answer is to the question using semantic similarity
        """
        question_embedding = self.embedder.encode(question)
        answer_embedding = self.embedder.encode(answer)
        
        similarity = cosine_similarity([question_embedding], [answer_embedding])[0][0]
        return float(similarity)
    
    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        """
        Evaluate how faithful the answer is to the retrieved context
        Simple implementation using semantic similarity
        """
        if not context.strip():
            return 0.0
            
        answer_embedding = self.embedder.encode(answer)
        context_embedding = self.embedder.encode(context)
        
        similarity = cosine_similarity([answer_embedding], [context_embedding])[0][0]
        return float(similarity)
    
    def evaluate_with_llm_judge(self, question: str, answer: str, context: str) -> Dict:
        """
        Use LLM as a judge to evaluate answer quality
        """
        if not groq_client:
            return {"error": "LLM client not available"}
            
        judge_prompt = f"""
You are an expert evaluator. Please evaluate the following Q&A based on the given context.

Question: {question}
Answer: {answer}
Context: {context[:1000]}...

Please rate the answer on a scale of 1-5 for each criterion:
1. Relevance: How well does the answer address the question?
2. Accuracy: Is the answer factually correct based on the context?
3. Completeness: Does the answer fully address the question?
4. Clarity: Is the answer clear and well-structured?

Respond in JSON format:
{{"relevance": <score>, "accuracy": <score>, "completeness": <score>, "clarity": <score>, "explanation": "<brief explanation>"}}
"""
        
        try:
            response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": judge_prompt}],
                model="llama3-8b-8192",
                temperature=0.1,
                max_tokens=300
            )
            
            # Try to parse JSON response
            response_text = response.choices[0].message.content
            # Extract JSON from response (simple approach)
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                return {"error": "Could not parse LLM response", "raw_response": response_text}
                
        except Exception as e:
            return {"error": f"LLM evaluation failed: {str(e)}"}
    
    def run_single_evaluation(self, question_data: Dict, index) -> Dict:
        """Run evaluation for a single question"""
        question = question_data['question']
        print(f"\n🔍 Evaluating: {question}")
        
        # Get RAG response (simulate the query function)
        start_time = time.time()
        
        # Query the system
        query_embedding = self.embedder.encode(question).tolist()
        search_results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True,
            namespace="rag-proj"
        )
        
        # Generate response
        response = generate_response(question, search_results.matches)
        response_time = time.time() - start_time
        
        # Prepare context for evaluation
        context = "\n".join([match.metadata.get('text', '') for match in search_results.matches])
        
        # Run evaluations
        retrieval_eval = self.evaluate_retrieval(
            question, 
            search_results.matches, 
            question_data.get('relevant_sources', [])
        )
        
        answer_relevance = self.evaluate_answer_relevance(question, response)
        faithfulness = self.evaluate_faithfulness(response, context)
        llm_judge = self.evaluate_with_llm_judge(question, response, context)
        
        result = {
            'question_id': question_data['id'],
            'question': question,
            'category': question_data.get('category', ''),
            'difficulty': question_data.get('difficulty', ''),
            'generated_answer': response,
            'response_time': response_time,
            'retrieval_evaluation': retrieval_eval,
            'answer_relevance': answer_relevance,
            'faithfulness': faithfulness,
            'llm_judge_scores': llm_judge,
            'retrieved_context': context[:500] + "..." if len(context) > 500 else context
        }
        
        return result
    
    def run_full_evaluation(self, test_questions_path: str, index, output_path: str = None):
        """Run evaluation on all test questions"""
        questions = self.load_test_questions(test_questions_path)
        print(f"🚀 Starting evaluation with {len(questions)} questions...")
        
        results = []
        for i, question_data in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}]", end="")
            result = self.run_single_evaluation(question_data, index)
            results.append(result)
            
        # Calculate aggregate metrics
        summary = self.calculate_summary_metrics(results)
        
        evaluation_report = {
            'summary': summary,
            'detailed_results': results,
            'evaluation_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save results
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(evaluation_report, f, indent=2)
            print(f"\n💾 Results saved to {output_path}")
        
        self.print_summary(summary)
        return evaluation_report
    
    def calculate_summary_metrics(self, results: List[Dict]) -> Dict:
        """Calculate aggregate metrics across all results"""
        if not results:
            return {}
            
        # Retrieval metrics
        avg_precision = np.mean([r['retrieval_evaluation']['precision_at_k'] for r in results])
        avg_similarity = np.mean([r['retrieval_evaluation']['avg_similarity_score'] for r in results])
        
        # Generation metrics
        avg_relevance = np.mean([r['answer_relevance'] for r in results])
        avg_faithfulness = np.mean([r['faithfulness'] for r in results])
        avg_response_time = np.mean([r['response_time'] for r in results])
        
        # LLM Judge metrics (if available)
        llm_scores = [r['llm_judge_scores'] for r in results if 'error' not in r['llm_judge_scores']]
        llm_summary = {}
        if llm_scores:
            llm_summary = {
                'avg_relevance': np.mean([s.get('relevance', 0) for s in llm_scores]),
                'avg_accuracy': np.mean([s.get('accuracy', 0) for s in llm_scores]),
                'avg_completeness': np.mean([s.get('completeness', 0) for s in llm_scores]),
                'avg_clarity': np.mean([s.get('clarity', 0) for s in llm_scores])
            }
        
        return {
            'num_questions': len(results),
            'retrieval_metrics': {
                'avg_precision_at_k': avg_precision,
                'avg_similarity_score': avg_similarity
            },
            'generation_metrics': {
                'avg_answer_relevance': avg_relevance,
                'avg_faithfulness': avg_faithfulness,
                'avg_response_time': avg_response_time
            },
            'llm_judge_metrics': llm_summary
        }
    
    def print_summary(self, summary: Dict):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("📊 RAG EVALUATION SUMMARY")
        print("="*60)
        
        print(f"📝 Total Questions: {summary['num_questions']}")
        print(f"⏱️  Avg Response Time: {summary['generation_metrics']['avg_response_time']:.2f}s")
        
        print("\n🔍 RETRIEVAL METRICS:")
        ret_metrics = summary['retrieval_metrics']
        print(f"  • Precision@3: {ret_metrics['avg_precision_at_k']:.3f}")
        print(f"  • Avg Similarity: {ret_metrics['avg_similarity_score']:.3f}")
        
        print("\n🤖 GENERATION METRICS:")
        gen_metrics = summary['generation_metrics']
        print(f"  • Answer Relevance: {gen_metrics['avg_answer_relevance']:.3f}")
        print(f"  • Faithfulness: {gen_metrics['avg_faithfulness']:.3f}")
        
        if summary.get('llm_judge_metrics'):
            print("\n👨‍⚖️ LLM JUDGE SCORES (1-5):")
            llm_metrics = summary['llm_judge_metrics']
            print(f"  • Relevance: {llm_metrics.get('avg_relevance', 0):.2f}/5")
            print(f"  • Accuracy: {llm_metrics.get('avg_accuracy', 0):.2f}/5")
            print(f"  • Completeness: {llm_metrics.get('avg_completeness', 0):.2f}/5")
            print(f"  • Clarity: {llm_metrics.get('avg_clarity', 0):.2f}/5")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    # Example usage
    print("RAG Evaluator - Run this script to evaluate your chatbot!")
    print("Make sure to:")
    print("1. Activate your virtual environment")
    print("2. Set up your Pinecone index")
    print("3. Run: python evaluation/rag_evaluator.py") 