from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_faiss_index(papers: list[dict]):
    """Create a LangChain FAISS vectorstore from a list of paper dicts."""
    texts = [p["summary"] for p in papers]
    vectorstore = FAISS.from_texts(texts, _embeddings, metadatas=papers)
    return vectorstore


def search_papers(query: str, vectorstore, top_k: int = 3) -> list[dict]:
    """Search the FAISS vectorstore and return matching paper dicts."""
    results = vectorstore.similarity_search(query, k=top_k)
    return [doc.metadata for doc in results]
