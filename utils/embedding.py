from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


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
            "id": "doc-{i}",
            "values": e
        })
    index.upsert(vectors=vectors, namespace="rag-proj")

    return embeddings


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

    print(result)