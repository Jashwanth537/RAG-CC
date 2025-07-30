from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize Groq client only if API key is available
groq_client = None
try:
    from groq import Groq
    if os.environ.get("GROQ_API_KEY"):
        groq_client = Groq()
        print("✅ Groq LLM client initialized successfully!")
    else:
        print("⚠️  GROQ_API_KEY not found. Running in retrieval-only mode.")
        print("💡 Make sure to set GROQ_API_KEY in your .env file")
except ImportError:
    print("⚠️  Groq not installed. Running in retrieval-only mode.")

def generate_embeddings(chunks, index):
# Load embedding model
    sentences = [x.page_content for x in chunks]
    # print("sentences: ")
    # print(sentences[:3])
    embeddings = embedder.encode(sentences)

    #map of embeddings and text
    vectors = []
    for i ,(chunk,e) in enumerate(zip(chunks, embeddings)): 
        vectors.append({
            "id": f"doc-{i}",
            "values": e.tolist(),
            "metadata": {
                "text": chunk.page_content,
                "source": chunk.metadata.get("source", "unknown")
            }
        })
    index.upsert(vectors=vectors, namespace="rag-proj")

    return embeddings


def generate_response(query, retrieved_chunks):
    """Generate a natural language response using Groq LLM"""
    
    # Check if Groq client is available
    if not groq_client:
        return "🔍 LLM response generation not available. Please set GROQ_API_KEY in your .env file to get AI-generated answers."
    
    # Prepare context from retrieved chunks
    context = "\n\n".join([
        f"Source: {chunk.metadata.get('source', 'unknown')}\n{chunk.metadata.get('text', '')}"
        for chunk in retrieved_chunks
    ])
    
    # Create prompt
    prompt = f"""You are a helpful assistant that answers questions about credit cards based on the provided documentation.

Context from credit card documents:
{context}

Question: {query}

Please provide a clear, accurate answer based on the provided context. If the context doesn't contain enough information to answer the question, please say so.

Answer:"""

    try:
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",  # Fast and free model
            temperature=0.1,  # Low temperature for more consistent answers
            max_tokens=500,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error generating response: {str(e)}"


def query(input, index): 
    #query the embedding model
    query_embedding = embedder.encode(input)
    query_embedding = query_embedding.tolist()
    # print(f"Query Embedding: {query_embedding}")
    result = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True, 
        namespace="rag-proj"
    )

    print("Query Results:")
    print(f"Input query: '{input}'")
    print("-" * 80)
    
    # Generate LLM response
    response = generate_response(input, result.matches)
    print(f"\n🤖 AI Response:")
    print(f"{response}")
    print("-" * 80)
    
    # Also show raw results for debugging
    for i, match in enumerate(result.matches, 1):
        print(f"\n--- Source {i} (Score: {match.score:.4f}) ---")
        print(f"Source: {match.metadata.get('source', 'unknown')}")
        print(f"Text: {match.metadata.get('text', 'No text available')[:200]}...")
        print("-" * 40)
    
    return result