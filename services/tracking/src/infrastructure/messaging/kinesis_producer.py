import os
import json
import boto3

from shared.logger import log_event, log_error

KINESIS_STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "tracking-events")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class KinesisProducerManager:
    def __init__(self):
        self.client = boto3.client("kinesis", region_name=AWS_REGION)

    async def send_event_to_kinesis(self, event: dict) -> bool:
        try:
            payload = json.dumps(event).encode("utf-8")
            partition_key = event.get("user_id", "default_partition")

            response = self.client.put_record(
                StreamName=KINESIS_STREAM_NAME,
                Data=payload,
                PartitionKey=partition_key,
            )
            log_event({"message": "Event sent to Kinesis", "response": response})
            return True
        except Exception as e:
            log_error(f"Error sending event to Kinesis: {str(e)}")
            return False


kinesis_manager = KinesisProducerManager()
