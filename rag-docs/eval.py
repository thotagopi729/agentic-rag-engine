from rag import answer, MIN_SCORE

# (question, any-of keywords the answer must contain; None = must refuse)
CASES = [
    ("What are the common attributes of an AI agent?", ["goal"]),
    ("What did Jensen Huang say about agents' computing power?", ["100"]),
    ("What happened with the Replit coding agent?", ["database"]),
    ("How did the city of Kyle, Texas use an AI agent?", ["Kyle", "311"]),
    ("What did the IAB Tech Lab publish?", ["AAMP", "Agentic Advertising"]),
    ("How did the Financial Times compare agent autonomy to self-driving cars?", ["SAE", "level"]),
    ("Who won the cricket world cup?", None),
    ("What is the capital of France?", None),
]


def passed(a, keys):
    low = a.lower()
    if keys is None:
        return "don't know" in low or "don’t know" in low
    return any(k.lower() in low for k in keys)


ok = 0
for q, keys in CASES:
    a = answer(q)
    good = passed(a, keys)
    ok += good
    print("PASS" if good else "FAIL", "-", q)

print(f"\nScore: {ok}/{len(CASES)}  (MIN_SCORE={MIN_SCORE})")