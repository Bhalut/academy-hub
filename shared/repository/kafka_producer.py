import json
import os

from kafka import KafkaProducer

from shared.logger import log_error
from services.tracking.src.app.schemas import EventSchema

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
except Exception as e:
    log_error(f"Failed to connect to Kafka: {str(e)}")
    producer = None


def send_event_to_kafka(event: EventSchema) -> bool:
    if producer is None:
        log_error("Kafka producer is not available")
        return False

    try:
        topic = f"tracking_{event.event_type}"
        producer.send(topic, event.model_dump(by_alias=True))
        producer.flush()
        return True
    except Exception as e:
        log_error(f"Error sending event to Kafka: {str(e)}")
        return False
