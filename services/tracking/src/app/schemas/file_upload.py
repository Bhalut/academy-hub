from pydantic import Field

from . import BaseEvent


class FileUploadEvent(BaseEvent):
    activity_id: str = Field(..., description="Activity ID associated with the file upload.")
    file_type: str = Field(..., description="Type of file uploaded (e.g., pdf, video).")
    file_size: float = Field(..., ge=0, description="Size of the uploaded file in bytes.")
    upload_status: str = Field(..., description="Status of the upload (e.g., completed, failed).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "timestamp": "2025-01-31T12:00:00Z",
                "activity_id": "activity_001",
                "file_type": "pdf",
                "file_size": 1048576,
                "upload_status": "completed"
            }
        }
    }
