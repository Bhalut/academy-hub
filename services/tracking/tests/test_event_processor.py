import pytest
from fastapi.testclient import TestClient

from services.tracking.src.application.services.event_processor import process_event
from services.tracking.src.interface.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_create_event_success():
    payload = {
        "event_type": "login",
        "user_id": "user123",
        "metadata": {"ip": "127.0.0.1"}
    }
    response = client.post("/events/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and data["message"] == "Event processed successfully"


@pytest.mark.asyncio
async def test_process_event_invalid():
    event_data = {"user_id": "user123", "metadata": {}}
    result = await process_event(event_data)
    assert "error" in result
