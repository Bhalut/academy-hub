from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import ORJSONResponse

from ...config.tasks import process_event_data

router = APIRouter()


@router.post("/process/", response_class=ORJSONResponse)
async def process_event(event: dict, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(process_event_data.delay, event)
        return ORJSONResponse(content={"message": "Event sent to processing queue"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
