import requests

def get_citations(title):
    """Fetch related works and citations using Semantic Scholar API."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}"
    response = requests.get(url).json()

    citations = [paper["title"] for paper in response.get("data", [])]
    return citations[:10]