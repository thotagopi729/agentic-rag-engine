import streamlit as st
from rag import answer

st.title("Chat with my notes")

if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

question = st.chat_input("Ask about the notes")
if question:
    st.session_state.history.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            reply = answer(question)
        except Exception as e:
            reply = f"Error: {e}"
        st.markdown(reply)
    st.session_state.history.append(("assistant", reply))