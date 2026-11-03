"""Keyword search over the local notes knowledge base."""

import re
from collections import Counter
from functools import lru_cache
from pathlib import Path


NOTES_PATH = Path(__file__).resolve().with_name("notes.txt")
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100
STOP_WORDS = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "did",
        "do", "does", "for", "from", "had", "has", "have", "how", "in",
        "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
        "were", "what", "when", "where", "which", "who", "why", "with",
    }
)


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks without breaking words unnecessarily."""
    if size < 1:
        raise ValueError("size must be greater than zero.")
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be non-negative and smaller than size.")

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text) and not text[end].isspace():
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)

    return chunks


@lru_cache(maxsize=1)
def _load_chunks() -> tuple[str, ...]:
    """Read and chunk notes.txt once per process."""
    try:
        text = NOTES_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Unable to read the knowledge base at {NOTES_PATH}: {exc}") from exc
    return tuple(chunk_text(text))


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"\w+", text.casefold())
        if token not in STOP_WORDS
    ]


def search(question: str, k: int = 4) -> list[tuple[float, str]]:
    """Return up to k matching chunks, ranked by query-term coverage."""
    if not isinstance(question, str):
        raise TypeError("question must be a string.")
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k must be a positive integer.")

    query_terms = set(_tokens(question))
    if not query_terms:
        return []

    scored_chunks: list[tuple[float, int, int, str]] = []
    for index, chunk in enumerate(_load_chunks()):
        term_counts = Counter(_tokens(chunk))
        matched_terms = sum(term in term_counts for term in query_terms)
        if matched_terms:
            score = matched_terms / len(query_terms)
            frequency = sum(term_counts[term] for term in query_terms)
            scored_chunks.append((score, frequency, index, chunk))

    scored_chunks.sort(key=lambda result: (-result[0], -result[1], result[2]))
    return [(score, chunk) for score, _, _, chunk in scored_chunks[:k]]
