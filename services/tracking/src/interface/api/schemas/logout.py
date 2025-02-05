from typing import Literal

from pydantic import Field

from .base import BaseEvent


class LogoutEvent(BaseEvent):
    event_type: Literal["logout"] = "logout"
    ip_address: str = Field(..., description="IP address of the user.")
    device: dict = Field(
        ...,
        description="Device details, including type (desktop/mobile), browser, and operating system.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user789",
                "timestamp": "2025-01-31T12:00:00Z",
                "ip_address": "192.168.1.1",
                "device": {"type": "desktop", "browser": "Firefox", "os": "Windows"},
            }
        }
    }
