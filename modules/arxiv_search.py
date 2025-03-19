import arxiv
import time
import numpy as np
from rank_bm25 import BM25Okapi

def fetch_arxiv_papers(query, year_range, topic, sort_by):
    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate if sort_by == "Newest" else arxiv.SortCriterion.Relevance
    )

    papers = []
    paper_texts = []
    for paper in search.results():
        time.sleep(1)
        year = paper.published.year 
        if year_range[0] <= year <= year_range[1]:  # Filter by year
            if topic == "All" or topic.lower() in paper.title.lower():  # Filter by topic
                papers.append({"title": paper.title, "summary": paper.summary, "url": paper.pdf_url})
                paper_texts.append(paper.title + " " + paper.summary)

    if not papers and sort_by == arxiv.SortCriterion.SubmittedDate:
        search = arxiv.Search(query=query, max_results=10, sort_by=arxiv.SortCriterion.Relevance)
        papers = list(search.results())

    if papers:
        ranked_papers = bm25_ranking(query, papers, paper_texts)
        return ranked_papers[:10]

    return papers

def bm25_ranking(query, papers, paper_texts):
    tokenized_corpus = [text.split() for text in paper_texts]
    bm25 = BM25Okapi(tokenized_corpus)

    query_tokens = query.split()
    bm25_scores = bm25.get_scores(query_tokens)

    # Rank papers by BM25 score
    ranked_indices = np.argsort(bm25_scores)[::-1] # Sort descending
    ranked_papers = [papers[i] for i in ranked_indices]

    return ranked_papers