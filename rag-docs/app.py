import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Agentic RAG Assistant")
st.write("Ask anything about AI Agents based on our knowledge base!")

# Render API URL (మన లైవ్ లింక్)
API_URL = "https://agentic-rag-engine-4tb0.onrender.com/ask"

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History from History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])
                    
                    # Format output with answer and sources
                    full_response = f"{answer}\n\n**Sources:** {', '.join(sources) if sources else 'None'}"
                else:
                    full_response = f"⚠️ Error from server: Status code {response.status_code}"
            except Exception as e:
                full_response = f"⚠️ Connection error: {e}"
            
            st.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})