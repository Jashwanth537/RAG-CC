# Base LM ? 
# Hugging face token
# break document into chunks/convert into embeddings and store in a vector db. 
#ReAct framework : Reason/ Action - what about COT, lets keep it too. 
#Scale of context/data for RAG? 

# pinecone
# langchain
# huggingface
# v2: fastapi if complete fullstack app
# v3: Dockerrise. 
import os
import time
from pinecone import (Pinecone, ServerlessSpec,CloudProvider,AwsRegion,VectorType)
from utils.pdf_utils import extract_docs
from pathlib import Path
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import torch
load_dotenv()

base_dir = Path(__file__).resolve().parent.parent  # This gives project root
pdf_dir = base_dir / "data" / "pdfs"

chunks = extract_docs(pdf_dir, 500, 50)

# print(f"{chunks[9]}")


#Vector db pinecone setup
pc = Pinecone(os.environ.get("PINECONE_API_KEY"))
index_name = "ragproj-v1"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud= CloudProvider.AWS,
            region=AwsRegion.US_EAST_1
        ), 
        vector_type=VectorType.DENSE
    )
#connect to the index
index = pc.Index(index_name)
time.sleep(1)
index.describe_index_stats()
# Load embedding model
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
sentences = [x.page_content for x in chunks]
# print("sentences: ")
# print(sentences[:3])
embeddings = embedder.encode(sentences)

#map of embeddings and text
vectors = []
for i ,(chunk,e) in enumerate(zip(chunks, embeddings)): 
    vectors.append({
        "id": "doc-{i}",
        "values": e
    })
index.upsert(vectors=vectors, namespace="rag-proj")


#query the embedding model
query = input("Please Enter your query\n")
query_embedding = embedder.encode(query)
query_embedding = query_embedding.tolist()
# print(f"Query Embedding: {query_embedding}")
result = index.query(
    vector=query_embedding,
    top_k=3,
    include_metadata=True, 
    namespace="rag-proj"
)

print(result)





