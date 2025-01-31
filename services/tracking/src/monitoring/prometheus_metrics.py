from prometheus_client import Counter, Histogram, Gauge

EVENTS_PROCESSED = Counter("events_processed_total", "Total events processed")
EVENTS_FAILED = Counter("events_failed_total", "Total failed events")
REQUEST_LATENCY = Histogram("request_latency_seconds", "HTTP Request Latency")
ACTIVE_TASKS = Gauge("active_celery_tasks", "Number of active tasks in Celery")


def update_active_tasks(count: int):
    ACTIVE_TASKS.set(count)
