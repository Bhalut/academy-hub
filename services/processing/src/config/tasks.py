import os

import httpx

from shared.logger import log_event, log_error
from .celery_config import celery_app

STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://storage:8040")


@celery_app.task(name="process_event_data")
def process_event_data(event_data: dict):
    try:
        log_event(event_data)
        print(f"Processing event: {event_data}")

        with httpx.Client() as client:
            response = client.post(f"{STORAGE_SERVICE_URL}/store/processed/", json=event_data)
            response.raise_for_status()

        return {"status": "processed"}
    except Exception as e:
        log_error(f"Failed processing event: {str(e)}")
        raise e
