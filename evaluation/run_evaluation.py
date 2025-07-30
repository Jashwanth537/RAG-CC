 #!/usr/bin/env python3
"""
Quick evaluation runner for RAG chatbot
Usage: python evaluation/run_evaluation.py
"""

import os
import sys
sys.path.append('..')

from dotenv import load_dotenv
from pinecone import Pinecone
from rag_evaluator import RAGEvaluator

# Load environment variables
load_dotenv()

def main():
    print("🚀 RAG Chatbot Evaluation")
    print("=" * 40)
    
    # Initialize Pinecone
    try:
        pc = Pinecone(os.environ.get("PINECONE_API_KEY"))
        index = pc.Index("ragproj-v1")
        print("✅ Connected to Pinecone")
    except Exception as e:
        print(f"❌ Failed to connect to Pinecone: {e}")
        return
    
    # Initialize evaluator
    evaluator = RAGEvaluator()
    
    # Run evaluation
    try:
        results = evaluator.run_full_evaluation(
            test_questions_path="evaluation/test_questions.json",
            index=index,
            output_path="evaluation/evaluation_results.json"
        )
        
        print("\n✅ Evaluation completed successfully!")
        print("📁 Check evaluation/evaluation_results.json for detailed results")
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 