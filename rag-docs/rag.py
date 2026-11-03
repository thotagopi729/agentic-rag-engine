from memory import load_memory

def answer_with_history(messages):
    api_key = _get_api_key()
    if not api_key:
        return "API Key missing!"

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    
    latest_question = messages[-1]["content"] if messages else ""
    
    # నాలెడ్జ్ బేస్ నుండి నోట్స్ తీసుకోవడం
    search_results = search(latest_question, k=2)
    context_text = "\n".join([chunk for _, chunk in search_results]) if search_results else ""

    # పర్మినెంట్ యూజర్ మెమరీని లోడ్ చేయడం
    user_memory = load_memory()

    # సిస్టమ్ ప్రాంప్ట్‌లో మెమరీని కూడా ఇన్‌క్లూడ్ చేయడం
    SYSTEM_PROMPT = (
        "You are a friendly, intelligent, and helpful AI assistant, like Gemini. "
        f"Here is what you remember about the user and their preferences:\n{user_memory}\n\n"
        "Use the provided context or memory if it helps answer the user's question accurately."
    )

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\n\nContext notes:\n{context_text}"}]
    
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model=MODEL,
        messages=api_messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()