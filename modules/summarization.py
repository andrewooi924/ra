from openai import OpenAI
from modules.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text):
    """Summarize academic paper text using GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI research assistant that summarizes academic papers."},
            {"role": "user", "content": f"Summarize this academic paper: {text}"}
        ]
    )
    return response.choices[0].message.content

def summarize_paper_sections(text):
    """Summarize key sections: Abstract, Methodology, Key Findings."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the paper in three parts: Abstract, Methodology, Key Findings."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content
