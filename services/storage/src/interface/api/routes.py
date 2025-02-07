from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from ..infrastructure.repository import StorageRepository

router = APIRouter()
storage_repo = StorageRepository()


@router.post("/store/raw/")
async def store_raw_event(event: dict):
    try:
        result = await storage_repo.insert_raw("tracking_events", event)
        return ORJSONResponse(content={"message": "Raw event stored successfully", "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store/processed/")
def store_processed_event(event: dict):
    try:
        result = storage_repo.insert_processed("processed_events", event)
        return ORJSONResponse(content={"message": "Processed event stored successfully", "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
