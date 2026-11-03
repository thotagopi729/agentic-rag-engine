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
    ("How much computing power would agents need compared to chatbots?", ["100"]),
    ("When did the Food and Drug Administration announce its agentic AI plans?", ["December 2025"]),
    ("How much money did the Replit incident cost the company?", None),
    # --- 1. Paraphrase Cases (3) ---
    # Tests semantic understanding by swapping article phrasing for synonyms
    (
        "Which video games have researchers used as virtual environments to train autonomous systems?",
        ["Minecraft", "No Man's Sky"],
    ),
    (
        "What went wrong when a Replit programming tool was tested during a code freeze?",
        ["production database"],
    ),
    (
        "What standard did Anthropic release in late 2024 to help language models connect with external tools?",
        ["Model Context Protocol", "MCP"],
    ),

    # --- 2. Buried Detail Cases (3) ---
    # Tests retrieval precision on specific names, dates, and numbers inside paragraphs
    (
        "Who authored the 1958 'Pandemonium' paper that laid early theoretical groundwork for agent architecture?",
        ["Oliver Selfridge"],
    ),
    (
        "Which computer scientist helped popularize the word 'agentic' in 2024?",
        ["Andrew Ng"],
    ),
    (
        "Which organization formed the Agentic AI Foundation (AAIF) in December 2025?",
        ["Linux Foundation"],
    ),

    # --- 3. Near-Miss Refusal Cases (2) ---
    # High keyword overlap with notes.txt, but the specific fact is absent (expects None / "I don't know")
    (
        "How many FDA employees were granted access to agentic AI capabilities in December 2025?",
        None,
    ),
    (
        "What was the initial membership fee required for companies to join the Agentic AI Foundation?",
        None,
    ),
    
    
]


def norm(s):
    return (s.lower()
             .replace("\u202f", " ").replace("\u00a0", " ")
             .replace("\u2011", "-"))


def passed(a, keys):
    low = norm(a)
    if keys is None:
        return "don't know" in low or "don’t know" in low
    return any(norm(k) in low for k in keys)


ok = 0
for q, keys in CASES:
    a = answer(q)
    good = passed(a, keys)
    ok += good
    print("PASS" if good else "FAIL", "-", q)
    if not good:
        print("   ANSWER:", a[:200])

print(f"\nScore: {ok}/{len(CASES)}  (MIN_SCORE={MIN_SCORE})")