"""
Simple RAG Evaluation - Quick Test
Run individual questions and see detailed results
"""

import os
import sys
sys.path.append('..')

from dotenv import load_dotenv
from pinecone import Pinecone
from utils.embedding import generate_response, embedder
import time

load_dotenv()

def evaluate_single_question(question: str, expected_category: str = ""):
    """Evaluate a single question and show detailed results"""
    
    print(f"\n🔍 Question: {question}")
    print("=" * 60)
    
    # Connect to Pinecone
    pc = Pinecone(os.environ.get("PINECONE_API_KEY"))
    index = pc.Index("ragproj-v1")
    
    # Time the query
    start_time = time.time()
    
    # Get embeddings and search
    query_embedding = embedder.encode(question).tolist()
    search_results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True,
        namespace="rag-proj"
    )
    
    # Generate response
    response = generate_response(question, search_results.matches)
    
    end_time = time.time()
    
    # Display results
    print(f"⏱️  Response Time: {end_time - start_time:.2f}s")
    print(f"📝 Category: {expected_category}")
    
    print(f"\n🤖 Generated Answer:")
    print("-" * 40)
    print(response)
    
    print(f"\n📚 Retrieved Sources:")
    print("-" * 40)
    for i, match in enumerate(search_results.matches, 1):
        source = match.metadata.get('source', 'Unknown')
        similarity = match.score
        text_preview = match.metadata.get('text', '')[:100] + "..."
        
        print(f"{i}. {source} (Score: {similarity:.3f})")
        print(f"   Preview: {text_preview}")
        print()
    
    # Manual evaluation prompts
    print("🔍 Manual Evaluation:")
    print("-" * 40)
    print("Rate the following (1-5):")
    print("1. Is the answer relevant to the question?")
    print("2. Is the answer accurate based on the sources?")
    print("3. Is the answer complete?")
    print("4. Is the answer clear and well-structured?")
    
    return {
        'question': question,
        'answer': response,
        'response_time': end_time - start_time,
        'sources': [m.metadata.get('source', '') for m in search_results.matches],
        'similarity_scores': [m.score for m in search_results.matches]
    }

def main():
    """Run quick evaluation with sample questions"""
    
    sample_questions = [
        ("What is the annual fee for HDFC MoneyBack+ card?", "fees"),
        ("Which card offers the best cashback for online shopping?", "rewards"),
        ("Can I get a credit card with a salary of 25,000 rupees?", "eligibility"),
        ("What happens if I miss my credit card payment deadline?", "policies")
    ]
    
    print("🚀 RAG Chatbot - Quick Evaluation")
    print("=" * 50)
    
    results = []
    for question, category in sample_questions:
        result = evaluate_single_question(question, category)
        results.append(result)
        
        # Ask user for feedback
        print("\n⭐ Quick Rating (optional, press Enter to skip):")
        try:
            relevance = input("Relevance (1-5): ").strip()
            accuracy = input("Accuracy (1-5): ").strip()
            if relevance:
                result['manual_relevance'] = int(relevance)
            if accuracy:
                result['manual_accuracy'] = int(accuracy)
        except:
            pass
        
        print("\n" + "="*60)
    
    # Summary
    print("\n📊 QUICK SUMMARY:")
    print("-" * 30)
    avg_response_time = sum(r['response_time'] for r in results) / len(results)
    avg_similarity = sum(sum(r['similarity_scores']) / len(r['similarity_scores']) for r in results) / len(results)
    
    print(f"Average Response Time: {avg_response_time:.2f}s")
    print(f"Average Similarity Score: {avg_similarity:.3f}")
    print(f"Questions Evaluated: {len(results)}")
    
    if any('manual_relevance' in r for r in results):
        manual_ratings = [r.get('manual_relevance', 0) for r in results if r.get('manual_relevance')]
        if manual_ratings:
            print(f"Average Manual Relevance: {sum(manual_ratings)/len(manual_ratings):.1f}/5")

if __name__ == "__main__":
    main() 