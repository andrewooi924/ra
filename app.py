import streamlit as st
from modules.database import store_search, get_search_history
from modules.arxiv_search import fetch_arxiv_papers
from modules.embeddings import create_faiss_index, search_papers
from modules.pdf_processing import extract_full_text
from modules.summarization import summarize_paper_sections
from modules.citations import get_citations

# Streamlit UI
st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("AI Research Assistant")
st.sidebar.header("Filters")

# Sidebar Filters
year_filter = st.sidebar.slider("Select Year", 2000, 2024, (2015, 2024))
topic_filter = st.sidebar.selectbox("Topic", ["All", "AI", "NLP", "LLM"])
sort_by = st.sidebar.radio("Sort By", ["Relevance", "Newest"], index=0)

if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}

query = st.text_input("Enter your research topic")
col1, col2 = st.columns([1,2])
with col1:
    if st.button("Search") and query.strip():
        with st.spinner("Fetching papers..."):
            # Fetch papers and build FAISS index
            papers = fetch_arxiv_papers(query, year_filter, topic_filter, sort_by)
            st.session_state.papers = papers
            store_search(query)

            if not papers:
                st.warning("No papers found. Please try a different query or adjust filters.")
# with col2:
#     if st.button("Cite") and query.strip():
#         related_papers = get_citations(query)
#         st.write("**Related Papers:**")
#         for p in related_papers:
#             st.write(f"- {p}")

if "summaries_visible" not in st.session_state:
    st.session_state.summaries_visible = {}  # Track visibility per paper
summarize_pressed = False

if st.session_state.papers:
    st.subheader("Search Results")
    for paper in st.session_state.papers:
        col1, col2, col3 = st.columns([4,1,1])

        with col1:
            if st.button(paper["title"], key=f"toggle_{paper['title']}"):
                # Toggle summary visibility in session state
                st.session_state.summaries_visible[paper["title"]] = not st.session_state.summaries_visible.get(paper["title"], False)
        
        with col2:
            st.markdown(f"[PDF]({paper['url']})", unsafe_allow_html=True)

        with col3:
            if st.button("Summarize", key=paper["title"]):
                summarize_pressed = True

        with st.expander(paper["title"]):
            if summarize_pressed:
                with col1:
                    with st.spinner("Summarizing..."):
                        full_text = extract_full_text(paper["url"])
                        summary = summarize_paper_sections(full_text)
                        st.session_state.summaries[paper['title']] = summary
                        st.session_state.summaries_visible[paper["title"]] = True
                        summarize_pressed = False

        if st.session_state.summaries_visible.get(paper["title"], False):
            st.write(st.session_state.summaries.get(paper['title'], "Please press Summarize to summarize the paper."))

st.sidebar.header("Search History")
history = get_search_history()

for q, t in history:
    st.sidebar.write(f"{t}: {q}")