# RAG Document QA (Streamlit + Groq + Keyword Search)

A Retrieval-Augmented Generation (RAG) chatbot built over the local `notes.txt` knowledge base.

## Architecture
- **Retrieval (`search.py`)**: Reads `notes.txt` relative to the source file's absolute location, chunks it, and ranks matches by keyword coverage.
- **Answer generation (`rag.py`)**: Uses the Groq-compatible OpenAI client, applies `MIN_SCORE`, cites retrieved context, and abstains when no relevant chunks are found.
- **Chat UI (`app.py`)**: Maintains conversation history in Streamlit session state.
- **REST API (`api.py`)**: The optional FastAPI interface exposes `GET /health` and `POST /ask`.

## Quickstart
1. Install dependencies: `python -m pip install -r requirements.txt`
2. Set `GROQ_API_KEY` in Streamlit secrets or the environment.
3. Start the chat app: `streamlit run app.py`

The optional API can be started with `python -m uvicorn api:app --reload`.
