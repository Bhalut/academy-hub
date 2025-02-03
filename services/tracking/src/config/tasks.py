from shared.logger import log_error, log_event
from shared.metrics import EVENTS_FAILED, EVENTS_PROCESSED

from .celery_config import celery_app


@celery_app.task(name="process_event_data")
def process_event_data(event_data: dict):
    try:
        log_event(event_data)
        print(f"Processing event: {event_data}")
        EVENTS_PROCESSED.inc()
        return {"status": "processed"}
    except Exception as e:
        EVENTS_FAILED.inc()
        log_error(f"Failed processing event: {str(e)}")
        raise e
