import motor.motor_asyncio
from fastapi import HTTPException

from shared.logger import log_error
from ..config.settings import settings

MONGO_URI = settings.mongo_uri

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client["tracking"]
except Exception as e:
    log_error(f"Failed to connect to MongoDB: {str(e)}")
    client = None


async def save_event(collection_name: str, event: dict) -> bool:
    if client is None:
        log_error("MongoDB is not available")
        raise HTTPException(status_code=500, detail="MongoDB is not available")

    try:
        if not collection_name:
            log_error("Invalid collection name")
            return False

        collection = db[collection_name]
        result = await collection.insert_one(event)
        return result.acknowledged
    except Exception as e:
        log_error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
