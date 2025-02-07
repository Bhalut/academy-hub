import asyncio

from shared.logger import log_error, log_event
from ...infrastructure.factory import Factory

EVENT_BUFFER = []
BUFFER_SIZE = 10
LOCK = asyncio.Lock()


async def process_event(event_data: dict):
    try:
        async with LOCK:
            EVENT_BUFFER.append(event_data)

            if len(EVENT_BUFFER) < BUFFER_SIZE:
                return {"status": "buffered", "current_size": len(EVENT_BUFFER)}

            events_to_insert = EVENT_BUFFER[:]
            EVENT_BUFFER.clear()

        repo = Factory.get_repository()
        collection = "batch_events"
        result = await repo.insert_many(collection, events_to_insert)
        log_event({"message": f"Inserted {len(events_to_insert)} events in batch"})
        return {"inserted_count": len(events_to_insert)}
    except Exception as e:
        log_error(f"Error in batch insert: {str(e)}")
        return {"error": str(e)}
