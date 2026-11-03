from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rag import answer, MIN_SCORE, MODEL

app = FastAPI(
    title="RAG Docs API",
    description="Question-answering API over AI Agent documentation using Groq and vector search.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="The question to ask the RAG pipeline.",
        examples=["What standard did Anthropic release in late 2024?"],
    )


class AnswerResponse(BaseModel):
    question: str
    answer: str
    model: str
    min_score: float


@app.get("/health")
def health_check():
    return {"status": "ok", "model": MODEL, "min_score": MIN_SCORE}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be blank.")
    
    reply = answer(q)
    return AnswerResponse(
        question=q,
        answer=reply,
        model=MODEL,
        min_score=MIN_SCORE,
    )