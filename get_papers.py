import arxiv
import faiss
import fitz
import numpy as np
from openai import OpenAI
import os
import requests
from sentence_transformers import SentenceTransformer
import streamlit as st

# Load OpenAI client
api_key = os.environ["OPENAI_API_KEY"]

# Check for API key
if not api_key:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = OpenAI(api_key=api_key)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Fetch AI-related papers from arXiv
search = arxiv.Search(
    query="artificial intelligence",
    max_results=10,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Extract papers from arXiv
papers = []
paper_texts = []  # Store abstracts for embedding
for paper in search.results():
    papers.append({"title": paper.title, "summary": paper.summary, "url": paper.pdf_url})
    paper_texts.append(paper.summary)

# Convert summaries to embeddings
paper_embeddings = model.encode(paper_texts)

# Store in FAISS index
dimension = paper_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(paper_embeddings))

# Define search function
def search_papers(query, top_k=3):
    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding), top_k)
    
    results = [papers[i] for i in indices[0]]
    return results

# Summarize abstract
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a research assistant that summarizes academic papers."},
                  {"role": "user", "content": f"Summarize this academic paper: {text}"}]
    )
    return response.choices[0].message.content

# Extracct full text from paper
def extract_full_text(pdf_url):
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    # Read PDF
    doc = fitz.open("temp.pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"

    return full_text

# Summarize paper
def summarize_paper(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI research assistant. Summarize the paper with key sections."},
            {"role": "user", "content": f"Summarize this paper in three parts: \n\n1. Abstract\n2. Methodology\n3. Key Findings\n\n{text}"}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("AI Research Assistant")
query = st.text_input("Enter your research topic")

if st.button("Search"):
    results = search_papers(query)
    for paper in results:
        st.write(f"**{paper['title']}**")
        st.write(f"[PDF Link]({paper['url']})")
        # summary = summarize_text(paper["summary"])  # Summarize using GPT-4
        # st.write(f"**Summary:** {summary}")
        st.write(f'**Summary**: {summarize_paper(extract_full_text(paper['url']))}')

print("Research Completed!")