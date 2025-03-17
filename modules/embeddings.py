import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(papers):
    """Create FAISS index for paper embeddings."""
    paper_texts = [paper["summary"] for paper in papers]
    embeddings = model.encode(paper_texts)

    # Debugging: Check embeddings
    print("Embeddings shape:", np.array(embeddings).shape)  # Ensure 2D shape

    if len(embeddings) == 0:
        raise ValueError("No embeddings were generated. Check if paper summaries exist.")
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, papers

def search_papers(query, index, papers, top_k=3):
    """Search FAISS index for relevant papers."""
    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding), top_k)

    return [papers[i] for i in indices[0]]