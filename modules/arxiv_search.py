import arxiv

def fetch_arxiv_papers(query="deep learning OR machine learning OR MLP", max_results=10):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for paper in search.results():
        papers.append({
            "title": paper.title,
            "summary": paper.summary,
            "url": paper.pdf_url
        })

    return papers