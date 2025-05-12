
from pathlib import Path
import os
from utils.chunking import extract_docs
from utils.embedding import generate_embeddings
from utils.io import save_chunks_to_json, save_embeddings, load_embeddings, load_chunks_from_json

def prepare_data(index): 
    base_dir = Path(__file__).resolve().parent  # This gives project root
    pdf_dir = base_dir / "data" / "pdfs"


    chunks = extract_docs(pdf_dir, 500, 50)
    chunks_file = "saved/chunks.json"
    embeddings_file = "saved/embeddings.npy"

    if not os.path.exists(chunks_file):
        chunks = extract_docs("data/pdfs")
        save_chunks_to_json(chunks, chunks_file)
    else:
        chunks = load_chunks_from_json(chunks_file)
    # print(f"{chunks[9]}")
        
    if not os.path.exists(embeddings_file):
        embeddings = generate_embeddings(chunks, index)
        save_embeddings(embeddings, embeddings_file)
    else:
        from utils.io import load_embeddings
        embeddings = load_embeddings(embeddings_file)

