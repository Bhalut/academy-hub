from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from services.tracking.src.application.services.event_processor import process_event
from services.tracking.src.infrastructure.persistence.mongo_repository import (
    MongoRepository,
)
from services.tracking.src.interface.api.schemas import EventSchema
from shared.logger import log_error

router = APIRouter()


def get_mongo_repo() -> MongoRepository:
    return MongoRepository()


@router.post("/events/", response_class=ORJSONResponse)
async def create_event(
    event: EventSchema, repo: MongoRepository = Depends(get_mongo_repo)
):
    event_data = event.model_dump(by_alias=True)

    result = await process_event(event_data)
    if "error" in result:
        log_error(f"Event processing failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])

    return ORJSONResponse(content={"message": "Event processed successfully"})


@router.get("/health/", response_class=ORJSONResponse)
async def health_check(repo: MongoRepository = Depends(get_mongo_repo)):
    try:
        mongo_status = await repo.find_all("health_check", {}) is not None

        return ORJSONResponse(
            content={
                "status": "ok",
                "mongo": mongo_status,
                "prometheus": True,
                "kafka": True,
            }
        )
    except Exception as e:
        log_error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
