"""Answer questions using retrieved notes, permanent memory, and Groq API."""

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError

from search import search
from memory import load_memory

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.40"))
BASE_URL = "https://api.groq.com/openai/v1"

def _get_api_key() -> str:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except StreamlitSecretNotFoundError:
        api_key = None

    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError("GROQ_API_KEY is not configured.")
    return api_key.strip()

def answer_with_history(messages):
    """Passes full chat history, local context, and user memory to Groq."""
    if not messages:
        return "Hello! How can I help you today?"

    latest_question = messages[-1]["content"]
    
    # Search local notes knowledge base
    search_results = [r for r in search(latest_question, k=3) if r[0] >= MIN_SCORE]
    context_text = "\n\n".join([chunk for _, chunk in search_results]) if search_results else "No specific notes found."

    # Load permanent user memory
    user_memory = load_memory()

    SYSTEM_PROMPT = (
        "You are a friendly, intelligent, and helpful AI assistant, just like Gemini. "
        "You have access to long-term memory about the user and a local knowledge base.\n\n"
        f"**User Permanent Memory / Preferences:**\n{user_memory}\n\n"
        f"**Local Knowledge Base Context:**\n{context_text}\n\n"
        "Use the above information to answer the user accurately and conversationally."
    )

    client = OpenAI(api_key=_get_api_key(), base_url=BASE_URL)
    
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model=MODEL,
        messages=api_messages,
        temperature=0.7,
    )
    
    content = response.choices[0].message.content
    return content.strip() if content else "I couldn't generate a response."