import streamlit as st
from rag import answer, chat

st.title("Chat with my notes")

mode = st.sidebar.radio("Mode", ["Notes only (RAG)", "General chat"])

if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

question = st.chat_input("Ask a question")
if question:
    st.session_state.history.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            if mode == "Notes only (RAG)":
                reply = answer(question)
            else:
                msgs = [{"role": r, "content": t} for r, t in st.session_state.history]
                reply = chat(msgs)
        except Exception as e:
            reply = f"Error: {e}"
        st.markdown(reply)
    st.session_state.history.append(("assistant", reply))