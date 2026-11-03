"""Streamlit chat interface for the local-notes RAG assistant."""

import streamlit as st
from openai import OpenAIError

from rag import answer


st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agentic RAG Assistant")
st.caption("Ask questions about the information in the local knowledge base.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = answer(question)
            except (OpenAIError, RuntimeError, OSError, ValueError) as exc:
                st.error(f"Unable to answer this question: {exc}")
            else:
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
