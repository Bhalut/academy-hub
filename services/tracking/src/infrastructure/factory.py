import os

from ..infrastructure.messaging.kafka_producer import kafka_manager
from ..infrastructure.messaging.kinesis_producer import kinesis_manager
from ..infrastructure.persistence.dynamo_repository import DynamoRepository
from ..infrastructure.persistence.mongo_repository import MongoRepository


class Factory:
    @staticmethod
    def get_repository():
        environment = os.getenv("ENVIRONMENT", "development").lower()
        return DynamoRepository() if environment == "production" else MongoRepository()

    @staticmethod
    def get_messaging():
        environment = os.getenv("ENVIRONMENT", "development").lower()
        return kinesis_manager.send_event_to_kinesis if environment == "production" else kafka_manager.send_event_to_kafka
