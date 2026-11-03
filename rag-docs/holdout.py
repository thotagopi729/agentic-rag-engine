from rag import answer, MIN_SCORE

# (question, any-of keywords the answer must contain; None = must refuse)
CASES = [
   
    # --- 3 Answerable Cases (from the Government & Orchestration sections in notes.txt) ---
    (
        "Which Texas city deployed a Salesforce AI agent in March 2025 for 311 customer service?",
        ["Kyle"],
    ),
    (
        "What internal platform did the Department of Defense launch in December 2025 for intelligent agentic workflows?",
        ["GenAI.mil"],
    ),
    (
        "In agent orchestration, which iterative pattern has one agent generate a proposal while another evaluates it?",
        ["Planner-critic"],
    ),

    # --- 2 Near-Miss Refusal Traps (high keyword overlap, facts not in notes.txt) ---
    (
        "How many 311 customer service calls did the city of Kyle's AI agent handle in March 2025?",
        None,
    ),
    (
        "What was the total budget of the contract ICE signed in December 2025 for skip tracing AI agents?",
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