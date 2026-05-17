import time
import arxiv
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

_client = arxiv.Client(page_size=10, delay_seconds=10, num_retries=3)


def _fetch_with_backoff(search: arxiv.Search, max_attempts: int = 5) -> list:
    """Fetch results, retrying with exponential backoff on HTTP 429."""
    for attempt in range(max_attempts):
        try:
            return list(_client.results(search))
        except arxiv.HTTPError as e:
            if e.status == 429 and attempt < max_attempts - 1:
                wait = 15 * (2 ** attempt)  # 15s, 30s, 60s, 120s
                time.sleep(wait)
            else:
                raise


def fetch_arxiv_papers(query: str, year_range: tuple, topic: str, sort_by: str) -> list[dict]:
    sort_criterion = (
        arxiv.SortCriterion.SubmittedDate
        if sort_by == "Newest"
        else arxiv.SortCriterion.Relevance
    )
    search = arxiv.Search(query=query, max_results=10, sort_by=sort_criterion)

    papers, docs = [], []
    for paper in _fetch_with_backoff(search):
        year = paper.published.year
        if year_range[0] <= year <= year_range[1]:
            if topic == "All" or topic.lower() in paper.title.lower():
                meta = {"title": paper.title, "summary": paper.summary, "url": paper.pdf_url}
                papers.append(meta)
                docs.append(Document(page_content=paper.title + " " + paper.summary, metadata=meta))

    if not docs:
        fallback = arxiv.Search(query=query, max_results=10, sort_by=arxiv.SortCriterion.Relevance)
        for paper in _fetch_with_backoff(fallback):
            meta = {"title": paper.title, "summary": paper.summary, "url": paper.pdf_url}
            papers.append(meta)
            docs.append(Document(page_content=paper.title + " " + paper.summary, metadata=meta))

    if not docs:
        return []

    retriever = BM25Retriever.from_documents(docs, k=min(10, len(docs)))
    return [doc.metadata for doc in retriever.invoke(query)]