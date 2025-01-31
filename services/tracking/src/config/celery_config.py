from celery import Celery

celery_app = Celery(
    "tracking_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)

celery_app.conf.task_routes = {
    "app.tasks.process_event_data": {"queue": "events"},
}
