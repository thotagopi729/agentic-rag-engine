"""Persistent memory system to store user preferences and important facts."""

import os
from pathlib import Path

MEMORY_PATH = Path(__file__).resolve().with_name("user_memory.txt")

def load_memory() -> str:
    """Reads saved user memories and preferences."""
    if MEMORY_PATH.exists():
        text = MEMORY_PATH.read_text(encoding="utf-8").strip()
        if text:
            return text
    return "No prior user memory recorded."

def save_memory(new_info: str):
    """Appends new important user facts to memory."""
    if not new_info or not new_info.strip():
        return
    existing = load_memory()
    if existing == "No prior user memory recorded.":
        updated = f"- {new_info.strip()}"
    else:
        updated = f"{existing}\n- {new_info.strip()}"
    MEMORY_PATH.write_text(updated, encoding="utf-8")