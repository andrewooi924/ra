# AI Research Assistant

A Streamlit-based system for retrieving, ranking, and summarising academic papers, using BM25 and FAISS in LangChain for search and relevance scoring, an LLM for paper summarisation, and PostgreSQL for persistent search history.

## Features

* Query academic literature through a single interface
* BM25 lexical search
* FAISS vector search
* Combined ranking pipeline
* LLM-generated summaries
* Search history stored and retrievable from PostgreSQL

## Setup

### Creating an environment
1. Clone the repository.
2. Open a terminal and navigate to the project folder.
```
cd myproject
```
3. In your terminal, type:
```
python -m venv .venv
```
4. A folder named `.venv` will appear in your project. This directory is where your virtual environment and its dependencies are installed.

# Activating the environment
5. In your terminal, activate your environment with one of the following commands, depending on your operating system.
```bash
# Windows command prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS and Linux
source .venv/bin/activate
```

6. Once activated, you will see your environment name in parentheses before your prompt. `(.venv)`

### Installing dependencies
7. In the terminal with your environment activated, type:
```
pip install -r requirements.txt
```

8. Set the OpenAI API key using one of the following commands, depending on your operating system.
```
# Windows
setx OPENAI_API_KEY "your_key"

# macOS and Linux
export OPENAI_API_KEY="your_key"
```

### Running the application
9. Run the following command:
```
streamlit run app.py
```

10. The Streamlit app should appear in a new tab in your browser
<img width="2540" height="1257" alt="ra_image" src="https://github.com/user-attachments/assets/1cc77a20-afe9-477e-a73d-bf8928d94770" />
