import os
from dotenv import load_dotenv, find_dotenv

print("dotenv file found at:", find_dotenv())
load_dotenv()
key = os.getenv("GROQ_API_KEY")
print("loaded:", key is not None)
print("length:", len(key) if key else 0)
print("starts with gsk_:", bool(key and key.startswith("gsk_")))