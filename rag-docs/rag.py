import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from search import search

load_dotenv()

# Streamlit secrets నుంచి లేదా local env నుంచి GROQ_API_KEY తీసుకోవడం
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

client = OpenAI(
       api_key=api_key,
       base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-20b"
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.60"))

SYSTEM = (
    "Answer using ONLY the context provided. "
    "Cite sources like [1] or [2]. "
    "If the context does not contain the answer, say you don't know."
)


def answer(question):
    results = [r for r in search(question, k=4) if r[0] >= MIN_SCORE]
    if not results:
        return "I don't know based on the documents."

    context = "\n\n".join(
        f"[{i + 1}] {chunk}" for i, (score, chunk) in enumerate(results)
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        q = input("\nAsk (or 'quit'): ")
        if q == "quit":
            break
        print("\n" + answer(q))