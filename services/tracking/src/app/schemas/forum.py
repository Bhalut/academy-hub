from typing import Optional

from pydantic import Field

from . import BaseEvent


class ForumEvent(BaseEvent):
    forum_id: str = Field(..., description="Unique ID of the forum.")
    post_id: str = Field(..., description="Unique ID of the post.")
    action: str = Field(..., description="Action performed (e.g., created_post, liked, replied).")
    metadata: Optional[dict] = Field(default={}, description="Additional data specific to the forum interaction.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user456",
                "timestamp": "2025-01-31T12:00:00Z",
                "forum_id": "forum_123",
                "post_id": "post_456",
                "action": "liked",
                "metadata": {"comment": "Great discussion!"}
            }
        }
    }
