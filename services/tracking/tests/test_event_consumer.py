from ..events.kafka import consume_kafka_event

def test_kafka_consumer(mocker):
    mock_message = {"event_type": "click", "user_id": "123"}
    mocker.patch("kafka.KafkaConsumer.poll", return_value=[mock_message])

    event = consume_kafka_event()
    assert event["event_type"] == "click"
