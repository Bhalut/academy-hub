import json
import os

from kafka import KafkaConsumer

from .event_processor import process_event

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "tracking_events")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

for message in consumer:
    event_data = message.value
    print(f"Received event: {event_data}")
    process_event(event_data)
