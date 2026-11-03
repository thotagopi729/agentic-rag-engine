import sys
from search import search
from rag import answer, MIN_SCORE

question = " ".join(sys.argv[1:])

print("QUESTION:", question)
print(f"\nTop chunks (threshold = {MIN_SCORE}):")
for score, chunk in search(question, k=4):
    kept = "KEPT   " if score >= MIN_SCORE else "DROPPED"
    print(f"\n{kept} [{score:.3f}] {chunk[:250]}")

print("\nANSWER:\n" + answer(question))