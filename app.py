import streamlit as st
from modules.arxiv_search import fetch_arxiv_papers
from modules.embeddings import create_faiss_index, search_papers
from modules.pdf_processing import extract_full_text
from modules.summarization import summarize_paper_sections
from modules.citations import get_citations
from modules.database import init_db, save_search, get_search_history

# Initialize DB
init_db()

# UI Header
st.title("AI Research Assistant")
st.sidebar.header("Filters")

# Sidebar Filters
year_filter = st.sidebar.slider("Select Year", 2010, 2024, 2023)
topic_filter = st.sidebar.selectbox("Topic", ["AI", "NLP", "LLM"])
query = st.text_input("Enter your research topic")

if st.button("Search") and query.strip():
    # Fetch papers and build FAISS index
    papers = fetch_arxiv_papers(query)
    index, indexed_papers = create_faiss_index(papers)
    results = search_papers(query, index, indexed_papers)

    formatted_results = "\n".join([paper["title"] for paper in results])
    save_search(query, formatted_results)  # Save search to DB

    for paper in results:
        st.subheader(paper["title"])
        st.markdown(f"[PDF Link]({paper['url']})")

        full_text = extract_full_text(paper["url"])
        summary = summarize_paper_sections(full_text)
        st.write("**Summary:** \n", summary)

st.sidebar.header("Search History")
history = get_search_history()

for q, r in history:
    with st.sidebar.expander(q):
        st.write(r)

if st.button("Cite") and query.strip():
    related_papers = get_citations(query)
    st.write("**Related Papers:**")
    for p in related_papers:
        st.write(f"- {p}")