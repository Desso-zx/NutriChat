from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    """GET /health should report the service is up."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_query_happy_path():
    """A valid question should return a 200 with an answer and sources."""
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "How much sodium is recommended per day?"})
        assert response.status_code == 200

        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert len(data["answer"]) > 0


def test_query_invalid_input():
    """An empty question should be rejected with a 422 (Pydantic validation error)."""
    with TestClient(app) as client:
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 422


def test_query_missing_field():
    """A request missing the 'question' field entirely should also be a 422."""
    with TestClient(app) as client:
        response = client.post("/query", json={})
        assert response.status_code == 422