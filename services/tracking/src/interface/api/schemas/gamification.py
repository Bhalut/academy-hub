from typing import Literal

from pydantic import Field

from .base import BaseEvent


class GamificationEvent(BaseEvent):
    event_type: Literal["gamification"] = "gamification"
    course_id: str = Field(..., description="Associated course ID.")
    achievement_type: Literal["badge", "points", "level_up"] = Field(
        ..., description="Type of gamification event."
    )
    value: float = Field(..., description="Points or reward value.")
    description: str = Field(..., description="Description of the achievement.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user777",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course_567",
                "achievement_type": "badge",
                "value": 100,
                "description": "Completed all lessons in Module 1."
            }
        }
    }
