from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

router = APIRouter()

@router.get("/health/", response_class=ORJSONResponse)
async def health_check():
    return ORJSONResponse(
        content={
            "status": "ok",
            "kafka": True,
            "redis": True,
        }
    )
