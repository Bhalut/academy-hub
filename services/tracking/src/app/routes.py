from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from shared.logger import log_error
from shared.repository.mongo_repository import MongoRepository
from .schemas import EventSchema
from .services.event_processor import process_event

router = APIRouter()
repo = MongoRepository()


@router.post("/events/", response_class=ORJSONResponse)
async def create_event(event: EventSchema):
    event_data = event.model_dump(by_alias=True)

    result = await process_event(event_data)
    if "error" in result:
        log_error(f"Event processing failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])

    return ORJSONResponse(content={"message": "Event processed successfully"})


@router.get("/health/", response_class=ORJSONResponse)
async def health_check():
    try:
        mongo_status = await repo.find_all("health_check", {}) is not None

        return ORJSONResponse(
            content={
                "status": "ok",
                "mongo": mongo_status,
                "prometheus": True,
                "kafka": True
            }
        )
    except Exception as e:
        log_error(f"Health check failed: {str(e)}")
        return ORJSONResponse(
            content={
                "status": "error",
                "message": str(e)
            }
        )
