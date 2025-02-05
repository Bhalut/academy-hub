import datetime
import json
import os

from aiokafka import AIOKafkaProducer

from shared.logger import log_error, log_event
from ...interface.api.schemas import EventSchema

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


def default_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class KafkaProducerManager:
    def __init__(self):
        self.producer = None

    async def start(self):
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v, default=default_serializer).encode("utf-8"),
            )
            await self.producer.start()
            log_event({"message": "Kafka Producer started"})
        except Exception as e:
            log_error(f"Failed to connect to Kafka: {str(e)}")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            log_event({"message": "Kafka Producer stopped"})

    async def send_event_to_kafka(self, event: EventSchema) -> bool:
        if not self.producer:
            log_error("Kafka producer is not available")
            return False

        try:
            if hasattr(event, "model_dump"):
                payload = event.model_dump(by_alias=True)
            else:
                payload = event

            topic = f"tracking_{payload.get('event_type')}"
            await self.producer.send_and_wait(topic, payload)
            return True
        except Exception as e:
            log_error(f"Error sending event to Kafka: {str(e)}")
            return False


kafka_manager = KafkaProducerManager()
