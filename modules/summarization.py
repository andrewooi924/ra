from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from modules.config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

_summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI research assistant that summarizes academic papers."),
    ("user", "Summarize this academic paper: {text}")
])

_sections_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the paper in three parts: Abstract, Methodology, Key Findings."),
    ("user", "{text}")
])

_summarize_chain = _summarize_prompt | llm
_sections_chain = _sections_prompt | llm


def summarize_text(text: str) -> str:
    """Summarize academic paper text using GPT-4o-mini."""
    return _summarize_chain.invoke({"text": text}).content


def summarize_paper_sections(text: str) -> str:
    """Summarize key sections: Abstract, Methodology, Key Findings."""
    return _sections_chain.invoke({"text": text}).content
