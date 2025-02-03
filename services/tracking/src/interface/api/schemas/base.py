import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the event.",
    )
    user_id: str = Field(..., description="Unique identifier for the user.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of the event."
    )
    metadata: Optional[dict] = Field(
        None, description="Additional data specific to the event."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "metadata": {"source": "web"},
            }
        }
    }
