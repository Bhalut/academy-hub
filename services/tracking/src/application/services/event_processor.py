import datetime

from shared.logger import log_error, log_event
from ...config.tasks import process_event_data
from ...infrastructure.factory import Factory

repo = Factory.get_repository()
messaging = Factory.get_messaging()


def serialize_event_data(event_data):
    if isinstance(event_data, dict):
        return {key: serialize_event_data(value) for key, value in event_data.items()}
    elif isinstance(event_data, list):
        return [serialize_event_data(item) for item in event_data]
    elif isinstance(event_data, datetime.datetime):
        return event_data.isoformat()
    return event_data


async def process_event(event_data: dict):
    try:
        event_data = serialize_event_data(event_data)

        event_type = event_data.get("event_type")
        if not event_type:
            log_error("Invalid event: missing event_type")
            return {"error": "Invalid event: missing event_type"}

        collection_name = f"{event_type}_events"
        log_event(event_data)

        if not await messaging(event_data):
            log_error("Failed to send event")
            return {"error": "Failed to send event"}

        result = await repo.insert(collection_name, event_data)
        process_event_data.delay(event_data)

        return result
    except Exception as e:
        log_error(f"Error processing event: {str(e)}")
        return {"error": str(e)}
