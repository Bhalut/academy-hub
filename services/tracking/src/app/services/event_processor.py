from shared.logger import log_event, log_error
from shared.repository.mongo_repository import MongoRepository
from ...config.tasks import process_event_data
from shared.repository.kafka_producer import send_event_to_kafka

repo = MongoRepository()


async def process_event(event_data: dict):
    try:
        event_type = event_data.get("event_type")
        if not event_type:
            log_error("Invalid event: missing event_type")
            return {"error": "Invalid event: missing event_type"}

        collection_name = f"{event_type}_events"

        log_event(event_data)

        if not send_event_to_kafka(event_data):
            log_error("Failed to send event to Kafka")
            return {"error": "Failed to send event to Kafka"}

        result = await repo.insert(collection_name, event_data)
        process_event_data.delay(event_data)

        return result
    except Exception as e:
        log_error(f"Error processing event: {str(e)}")
        return {"error": str(e)}
