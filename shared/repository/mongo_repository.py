import os
from typing import Any, Dict, Optional

import motor.motor_asyncio
from fastapi import HTTPException

from .base_repository import BaseRepository
from ..logger import log_event, log_error

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["tracking"]


class MongoRepository(BaseRepository):
    async def insert(self, collection: str, data: Dict[str, Any]) -> bool:
        try:
            if "_id" in data:
                del data["_id"]
            result = await db[collection].insert_one(data)
            log_event({"mongo_insert_success": data})
            return result.acknowledged
        except Exception as e:
            log_error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def find_by_id(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        try:
            return await db[collection].find_one({"_id": id})
        except Exception as e:
            log_error(f"Database lookup error: {str(e)}")
            return None

    async def find_all(self, collection: str, filters: Dict[str, Any]) -> list:
        try:
            return await db[collection].find(filters).to_list(length=100)
        except Exception as e:
            log_error(f"Database query error: {str(e)}")
            return []
