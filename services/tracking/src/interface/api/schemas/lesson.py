from pydantic import Field

from .base import BaseEvent


class LessonEvent(BaseEvent):
    course_id: str = Field(..., description="Associated course ID.")
    lesson_id: str = Field(..., description="Unique ID for the lesson.")
    duration: float = Field(
        ..., ge=0, description="Time spent on the lesson in seconds."
    )
    completion_status: str = Field(
        ..., description="Completion status (e.g., completed, not_started)."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course_123",
                "lesson_id": "lesson_456",
                "duration": 1800,
                "completion_status": "completed",
            }
        }
    }
