"""Answer questions using retrieved notes and the Groq chat-completions API."""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError

from search import search

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.60"))
BASE_URL = "https://api.groq.com/openai/v1"
SYSTEM_PROMPT = (
    "Answer using only the supplied context. Cite supporting context with [1], [2], "
    "and so on. If the context does not contain the answer, say you don't know."
)
UNKNOWN_ANSWER = "I don't know based on the documents."


def _get_api_key() -> str:
    """Prefer Streamlit secrets, with environment variables as a local fallback."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except StreamlitSecretNotFoundError:
        api_key = None

    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to Streamlit secrets or the environment."
        )
    return api_key.strip()


def answer(question: str) -> str:
    """Retrieve relevant notes and generate a grounded answer with Groq."""
    if not isinstance(question, str):
        raise TypeError("question must be a string.")
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be blank.")

    results = [result for result in search(question) if result[0] >= MIN_SCORE]
    if not results:
        return UNKNOWN_ANSWER

    context = "\n\n".join(
        f"[{index}] {chunk}"
        for index, (_, chunk) in enumerate(results, start=1)
    )
    client = OpenAI(
        api_key=_get_api_key(),
        base_url=BASE_URL,
        timeout=30.0,
        max_retries=0,
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response.")
    return content.strip()
