from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from shared.logger import log_error
from ...application.services.event_processor import process_event
from ...interface.api.schemas import EventSchema
from ...security.auth import verify_token

router = APIRouter()


@router.post("/events/", response_class=ORJSONResponse)
async def create_event(
        event: EventSchema,
        _user=Depends(verify_token),
):
    event_data = event.model_dump(by_alias=True)
    result = await process_event(event_data)
    if "error" in result:
        log_error(f"Event processing failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])
    return ORJSONResponse(content={"message": "Event processed successfully"})


@router.get("/health/", response_class=ORJSONResponse)
async def health_check(
        _user=Depends(verify_token),
):
    try:
        return ORJSONResponse(
            content={
                "status": "ok",
            }
        )
    except Exception as e:
        log_error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
