import pytest
from app.main import app
import fastapi.testclient
print("fastapi.testclient path:", fastapi.testclient.__file__)
from fastapi.testclient import TestClient
print("TestClient class:", TestClient)

print("TestClient MRO:", TestClient.mro())
print("TestClient.__bases__:", TestClient.__bases__)
print("TestClient.__bases__[0]:", TestClient.__bases__[0])
print("TestClient.__bases__[0].__module__:", TestClient.__bases__[0].__module__)
print("TestClient.__bases__[0].__file__:", getattr(TestClient.__bases__[0], '__file__', 'N/A'))
client = TestClient(app)

def test_get_document_initial_state():
    response = client.get("/api/document")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["text"] == ""

def test_reset_document():
    client.post("/api/document/reset")
    response = client.get("/api/document")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == ""