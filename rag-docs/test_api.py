from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["min_score"] == 0.60


def test_ask_answerable_question():
    response = client.post(
        "/ask",
        json={"question": "What standard did Anthropic release in late 2024?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "Model Context Protocol" in data["answer"] or "MCP" in data["answer"]


def test_ask_refusal_question():
    response = client.post(
        "/ask",
        json={"question": "How much money did the Replit incident cost the company?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "don't know" in data["answer"].lower() or "do not know" in data["answer"].lower()


def test_ask_rejects_short_question():
    response = client.post("/ask", json={"question": "hi"})
    assert response.status_code == 422