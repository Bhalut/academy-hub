from fastapi.testclient import TestClient

from services.tracking.src.app.main import app

client = TestClient(app)


def test_create_event():
    response = client.post("/events/", json={
        "event_id": "123",
        "user_id": "user_456",
        "timestamp": "2025-01-27T16:00:00Z",
        "event_type": "click",
        "metadata": {"page": "home", "element_id": "btn_1"}
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Event processed successfully"
