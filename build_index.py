# build_index.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# --- Configuration ---
DOCS_DIR = Path("docs")
INDEX_DIR = Path("index_data")
DOCS_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)

# We use a reliable embedding model for medical/instructional text
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
LOCAL_MODEL_PATH = Path("models") / EMBED_MODEL_NAME

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Splits text into overlapping chunks based on word count."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def load_documents(doc_dir=DOCS_DIR):
    """Loads all .txt documents from the docs folder."""
    docs = []
    for file_path in doc_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            chunks = chunk_text(content)
            docs.extend(chunks)
    return docs

def build_index(docs, model):
    """Encodes documents and creates a FAISS index."""
    embeddings = model.encode(docs, show_progress_bar=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index, embeddings

def save_index_and_metadata(index, docs):
    """Saves the FAISS index and the associated text chunks."""
    faiss.write_index(index, str(INDEX_DIR / "faiss.index"))
    with open(INDEX_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(docs, f)

def main():
    print("Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL_NAME)
    
    print("Loading and chunking documents...")
    docs = load_documents()
    if not docs:
        print("No documents found in 'docs/' folder. Please add sample.txt.")
        return
        
    print(f"Building index for {len(docs)} text chunks...")
    index, _ = build_index(docs, model)
    
    print("Saving index to disk...")
    save_index_and_metadata(index, docs)
    print("Success! Index is ready for the RAG chatbot.")

if __name__ == "__main__":
    main()