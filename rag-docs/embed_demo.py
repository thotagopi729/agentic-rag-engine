from fastembed import TextEmbedding
import numpy as np

model = TextEmbedding("BAAI/bge-small-en-v1.5")

sentences = [
    "How do I reset my password?",
    "Steps to recover a forgotten login credential",
    "The cat sat on the sofa",
    "Pizza is my favourite food",
]

vectors = np.array(list(model.embed(sentences)))
print("Shape:", vectors.shape)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query = vectors[0]
for s, v in zip(sentences, vectors):
    print(round(float(cosine(query, v)), 3), s)