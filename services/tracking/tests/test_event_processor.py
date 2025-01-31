import pytest

from services.tracking.src.app.services.event_processor import process_event


@pytest.mark.asyncio
async def test_process_event():
    event_data = {
        "event_id": "123",
        "user_id": "user_456",
        "timestamp": "2025-01-27T16:00:00Z",
        "event_type": "click",
        "metadata": {"page": "home", "element_id": "btn_1"}
    }

    result = await process_event(event_data)
    assert result is True
