import numpy as np
from fastembed import TextEmbedding
from chunker import chunk_text

text = open("notes.txt", encoding="utf-8").read()
chunks = chunk_text(text)

model = TextEmbedding("BAAI/bge-small-en-v1.5")
chunk_vectors = np.array(list(model.passage_embed(chunks)))
print("Embedded", len(chunks), "chunks")


def search(question, k=3):
    q = np.array(list(model.query_embed(question)))[0]
    scores = chunk_vectors @ q / (
        np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(q)
    )
    top = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), chunks[i]) for i in top]


if __name__ == "__main__":
    while True:
        question = input("\nAsk (or 'quit'): ")
        if question == "quit":
            break
        for score, chunk in search(question):
            print(f"\n[{score:.3f}] {chunk[:300]}")