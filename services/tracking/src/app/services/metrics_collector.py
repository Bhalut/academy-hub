from shared.metrics import EVENTS_PROCESSED, EVENTS_FAILED


def collect_metrics(event_status: str):
    if event_status == "processed":
        EVENTS_PROCESSED.inc()
    else:
        EVENTS_FAILED.inc()
