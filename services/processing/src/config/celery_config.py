import os

from celery import Celery

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = os.getenv("REDIS_PORT", "6379")

celery_app = Celery(
    "processing_tasks",
    broker=f"redis://{redis_host}:{redis_port}/0",
    backend=f"redis://{redis_host}:{redis_port}/0",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)

celery_app.conf.task_routes = {
    "processing.tasks.process_event_data": {"queue": "events"},
}
