from typing import Literal, Optional

from pydantic import Field

from .base import BaseEvent


class ProgressEvent(BaseEvent):
    event_type: Literal["progress"] = "progress"
    course_id: str = Field(..., description="Associated course ID.")
    lesson_id: str = Field(..., description="Associated lesson ID.")
    progress_percentage: float = Field(..., ge=0, le=100, description="Completion percentage.")
    completion_status: str = Field(..., description="Status of progress (e.g., completed, in_progress).")
    time_spent: Optional[float] = Field(None, ge=0, description="Total time spent on the lesson in seconds.")
    interaction_type: Optional[str] = Field(None, description="Type of interaction (watched_video, read_text).")
    previous_progress: Optional[float] = Field(None, ge=0, le=100, description="Previous progress percentage.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "uuid_789",
                "user_id": "user_001",
                "timestamp": "2025-02-06T12:00:00Z",
                "course_id": "course_456",
                "lesson_id": "lesson_789",
                "progress_percentage": 75.5,
                "completion_status": "in_progress",
                "time_spent": 1200,
                "interaction_type": "watched_video",
                "previous_progress": 50.0
            }
        }
    }
