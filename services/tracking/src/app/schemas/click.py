from typing import Optional

from pydantic import Field

from . import BaseEvent


class ClickEvent(BaseEvent):
    course_id: Optional[str] = Field(None, description="Associated course ID.")
    page: str = Field(..., description="Page where the interaction occurred.")
    action: str = Field(..., description="Action performed (e.g., clicked, opened).")
    element_id: str = Field(..., description="Unique identifier of the interacted element.")
    metadata: Optional[dict] = Field(None, description="Additional metadata about the event.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "page": "home",
                "action": "clicked",
                "element_id": "btn_login",
                "metadata": {"css_class": "btn-primary"}
            }
        }
    }
