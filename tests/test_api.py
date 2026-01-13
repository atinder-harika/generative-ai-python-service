from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_analyze_code_success():
    payload = {
        "code": "def add(a, b):\n    return a + b",
        "language": "python"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)

def test_analyze_code_empty():
    payload = {
        "code": "",
        "language": "python"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 422

def test_analyze_code_with_context():
    payload = {
        "code": "class Stack:\n    pass",
        "language": "python",
        "context": "Data structure implementation"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    assert "analysis" in response.json()
