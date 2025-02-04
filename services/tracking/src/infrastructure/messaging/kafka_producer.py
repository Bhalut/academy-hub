import json
import os

from aiokafka import AIOKafkaProducer

from shared.logger import log_error
from ...interface.api.schemas import EventSchema

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")


class KafkaProducerManager:
    def __init__(self):
        self.producer = None

    async def start(self):
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self.producer.start()
            print("✅ Kafka Producer started")
        except Exception as e:
            log_error(f"❌ Failed to connect to Kafka: {str(e)}")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            print("🔴 Kafka Producer stopped")

    async def send_event_to_kafka(self, event: EventSchema) -> bool:
        if not self.producer:
            log_error("Kafka producer is not available")
            return False
        try:
            topic = f"tracking_{event.event_type}"
            await self.producer.send_and_wait(topic, event.model_dump(by_alias=True))
            return True
        except Exception as e:
            log_error(f"Error sending event to Kafka: {str(e)}")
            return False


kafka_manager = KafkaProducerManager()
