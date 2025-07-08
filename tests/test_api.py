import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_document():
    client.post("/api/document/reset")

def test_websocket_broadcast():
    with client.websocket_connect("/ws/clientA") as ws_a, client.websocket_connect("/ws/clientB") as ws_b:
        state_a = ws_a.receive_json()
        state_b = ws_b.receive_json()
        assert state_a["text"] == ""
        assert state_b["text"] == ""
        op = {
            "type": "insert",
            "char_id": "1:1:abc123",
            "char": "X",
            "parent_id": "root",
            "site_id": 1,
            "logical_timestamp": 1
        }
        ws_a.send_json(op)
        print("Waiting for ws_b to receive...")
        received_b = ws_b.receive_json()
        print("ws_b received:", received_b)
        assert received_b["type"] == "insert"
        assert received_b["char"] == "X"

def test_websocket_basic_connect():
    with client.websocket_connect("/ws/testclient1") as websocket:
        initial_state = websocket.receive_json()
        assert "text" in initial_state
        assert initial_state["text"] == ""

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