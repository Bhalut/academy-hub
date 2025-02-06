from typing import Optional, Literal

from pydantic import Field

from .base import BaseEvent


class LiveSessionEvent(BaseEvent):
    event_type: Literal["live_session"] = "live_session"
    session_id: str = Field(..., description="Unique ID for the live session.")
    course_id: str = Field(..., description="Associated course ID.")
    action: Literal["joined", "left", "sent_message", "raised_hand", "reacted"] = Field(
        ..., description="User action during the live session."
    )
    message_content: Optional[str] = Field(None, description="Message content if action is 'sent_message'.")
    reaction: Optional[str] = Field(None, description="User reaction (like, clap, emoji).")
    duration: Optional[float] = Field(None, ge=0, description="Time spent in the session in seconds.")
    stream_quality: Optional[str] = Field(None, description="Quality of the stream (1080p, 720p, etc.).")
    connection_status: Optional[str] = Field(None, description="Network connection status (good, poor, disconnected).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "uuid_123",
                "user_id": "user_456",
                "timestamp": "2025-02-06T12:00:00Z",
                "session_id": "session_001",
                "course_id": "course_567",
                "action": "reacted",
                "reaction": "👍",
                "stream_quality": "720p",
                "connection_status": "good",
                "duration": 1800
            }
        }
    }
