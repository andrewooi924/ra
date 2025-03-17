import fitz
import requests

def extract_full_text(pdf_url):
    """Download and extract full text from a PDF paper."""
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    doc = fitz.open("temp.pdf")
    full_text = "\n".join([page.get_text("text") for page in doc])

    return full_text