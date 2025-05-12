import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def extract_text_from_pdf(file_path):
    """Extracts full text from a single PDF."""
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def extract_docs(folder_path, chunk_size=500, chunk_overlap=50):
    """Extracts and chunks documents from all PDFs in a folder, returns list of Documents with metadata."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            raw_text = extract_text_from_pdf(file_path)
            chunks = splitter.create_documents([raw_text])
            
            # Attach metadata
            for chunk in chunks:
                chunk.id = {
                    "source": file
                }
            all_chunks.extend(chunks)

    return all_chunks
