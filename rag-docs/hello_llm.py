import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a concise tutor."},
        {"role": "user", "content": "Explain what an API is in 2 sentences."},
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)