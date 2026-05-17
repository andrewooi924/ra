import requests
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

# Number of chunks to pass to the LLM — keeps the summarization within context limits
_MAX_CHUNKS = 5


def extract_full_text(pdf_url: str) -> str:
    """Download a PDF and return the first ~15 000 chars of extracted text."""
    response = requests.get(pdf_url, timeout=30)
    response.raise_for_status()

    tmp_path = "temp.pdf"
    with open(tmp_path, "wb") as f:
        f.write(response.content)

    loader = PyMuPDFLoader(tmp_path)
    pages = loader.load()

    chunks = _splitter.split_documents(pages)
    return "\n\n".join(chunk.page_content for chunk in chunks[:_MAX_CHUNKS])
