import json
import os

from kafka import KafkaConsumer

from ...storage.mongo_repository import MongoRepository

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

consumer = KafkaConsumer(
    "tracking_click",
    "tracking_progress",
    "tracking_quiz",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

repo = MongoRepository()

for message in consumer:
    event = message.value
    repo.insert("raw_events", event)
