from typing import Optional, Literal

from pydantic import Field

from .base import BaseEvent


class ClickEvent(BaseEvent):
    event_type: Literal["click"] = "click"
    course_id: Optional[str] = Field(None, description="Associated course ID.")
    page: str = Field(..., description="Page where the interaction occurred.")
    action: str = Field(..., description="Action performed (e.g., clicked, opened).")
    element_id: str = Field(
        ..., description="Unique identifier of the interacted element."
    )
    scroll_position: Optional[float] = Field(None, ge=0, le=100, description="Scroll position in percentage.")
    hover_time: Optional[float] = Field(None, ge=0, description="Time hovered over element before clicking (ms).")
    device_orientation: Optional[str] = Field(
        None, description="Device orientation (portrait, landscape)."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "uuid_456",
                "user_id": "user_789",
                "timestamp": "2025-02-06T12:00:00Z",
                "page": "home",
                "action": "clicked",
                "element_id": "btn_login",
                "scroll_position": 80.5,
                "hover_time": 1200,
                "device_orientation": "portrait",
            }
        }
    }
