from typing import Optional, Literal

from pydantic import Field

from .base import BaseEvent


class AssignmentEvent(BaseEvent):
    event_type: Literal["assignment"] = "assignment"
    course_id: str = Field(..., description="Associated course ID.")
    assignment_id: str = Field(..., description="Unique ID for the assignment.")
    submission_status: str = Field(
        ..., description="Status of the submission (e.g., submitted, late)."
    )
    score: Optional[float] = Field(None, description="Score achieved, if applicable.")
    feedback: Optional[str] = Field(
        None, description="Feedback provided by the instructor."
    )
    metadata: Optional[dict] = Field(None, description="Additional metadata.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course789",
                "assignment_id": "assignment456",
                "submission_status": "submitted",
                "score": 95.0,
                "feedback": "Good job!",
                "metadata": {"source": "web"},
            }
        }
    }
