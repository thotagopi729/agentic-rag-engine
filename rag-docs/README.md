# RAG Document QA API (FastAPI + Groq + Vector Search)

A production-style Retrieval-Augmented Generation (RAG) system built over AI Agent documentation. It includes semantic chunking, cosine similarity filtering, an automated evaluation suite, holdout validation, a FastAPI REST interface, and Docker support.

## Architecture
- **Retrieval (search.py)**: Embeds document chunks (notes.txt, 58 chunks) and retrieves top matches via cosine similarity.
- **Defense-in-Depth Generation (rag.py)**: Filters chunks below MIN_SCORE = 0.60 and instructs the LLM (openai/gpt-oss-20b via Groq) to answer strictly from context with inline citations ([1], [2]) or abstain.
- **REST API (api.py)**: Exposes GET /health and POST /ask with Pydantic validation.

## Threshold Sweep & Evaluation Results
| MIN_SCORE | Eval Score (eval.py) | Holdout Score (holdout.py) | Key Observation |
| :--- | :--- | :--- | :--- |
| 0.70 | 15 / 19 | - | Too strict; drops valid paraphrase & buried-detail chunks |
| 0.65 | 18 / 19 | - | Baseline; misses the Replit paraphrase case |
| **0.60 (Chosen)** | **19 / 19** | **5 / 5** | **Optimal boundary: 100% accuracy on tuning & unseen holdout sets** |
| 0.55 | 19 / 19 | 5 / 5 | Prompt guard holds, but lower threshold risks noisy context |

## Quickstart
1. Install dependencies: python -m pip install -r requirements.txt
2. Start API server: python -m uvicorn api:app --reload
3. Run evaluations: python eval.py && python holdout.py
4. Run API tests: python -m pytest -v
