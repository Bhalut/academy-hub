import os

from ..infrastructure.messaging.kafka_producer import kafka_manager
from ..infrastructure.messaging.kinesis_producer import kinesis_manager


class Factory:
    @staticmethod
    def get_messaging():
        environment = os.getenv("ENVIRONMENT", "development").lower()
        return kinesis_manager.send_event_to_kinesis if environment == "production" else kafka_manager.send_event_to_kafka
