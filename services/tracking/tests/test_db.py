import pytest

from services.tracking.src.infrastructure.persistence.mongo_repository import MongoRepository


@pytest.mark.asyncio
async def test_insert_and_find():
    repo = MongoRepository()
    test_data = {"event_type": "test", "user_id": "test_user"}
    collection = "test_events"

    success = await repo.insert(collection, test_data)
    assert success is True

    results = await repo.find_all(collection, {"user_id": "test_user"})
    assert len(results) > 0
