from shared.metrics import EVENTS_FAILED, EVENTS_PROCESSED


def collect_metrics(event_status: str):
    if event_status == "processed":
        EVENTS_PROCESSED.inc()
    else:
        EVENTS_FAILED.inc()
