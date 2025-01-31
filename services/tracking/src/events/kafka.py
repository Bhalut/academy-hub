import json
import os

from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "tracking_events")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    group_id="tracking_group",
    auto_offset_reset="earliest"
)

for message in consumer:
    print(f"Received event: {message.value}")
