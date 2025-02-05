from typing import Optional, Literal

from pydantic import Field

from .base import BaseEvent


class FeedbackEvent(BaseEvent):
    event_type: Literal["feedback"] = "feedback"
    course_id: str = Field(..., description="Associated course ID.")
    feedback_type: str = Field(
        ..., description="Type of feedback (e.g., lesson, quiz)."
    )
    rating: int = Field(
        ..., ge=1, le=5, description="Rating provided by the user (1 to 5)."
    )
    comments: Optional[str] = Field(
        None, description="Additional comments from the user."
    )
    metadata: Optional[dict] = Field(None, description="Additional metadata.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course789",
                "feedback_type": "lesson",
                "rating": 4,
                "comments": "Great content!",
                "metadata": {"source": "mobile_app"},
            }
        }
    }
