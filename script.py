import arxiv

search = arxiv.Search(
    query="artificial intelligence",
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

papers = list(search.results())  # Convert generator to list

print(f"Found {len(papers)} papers.")
for paper in papers:
    print(f"Title: {paper.title}")
