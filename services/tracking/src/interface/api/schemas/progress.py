from pydantic import Field

from .base import BaseEvent


class ProgressEvent(BaseEvent):
    course_id: str = Field(..., description="Associated course ID.")
    lesson_id: str = Field(..., description="Associated lesson ID.")
    progress_percentage: float = Field(
        ..., ge=0, le=100, description="Completion percentage."
    )
    completion_status: str = Field(
        ..., description="Status of progress (e.g., completed, in_progress)."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user789",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course_456",
                "lesson_id": "lesson_789",
                "progress_percentage": 75.5,
                "completion_status": "in_progress",
            }
        }
    }
