from typing import Any, Dict, List, Optional

import motor.motor_asyncio
from fastapi import HTTPException

from shared.logger import log_error, log_event
from shared.repository.base_repository import BaseRepository
from ...config.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
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

    async def find_all(
            self, collection: str, filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        try:
            return await db[collection].find(filters).to_list(length=100)
        except Exception as e:
            log_error(f"Database query error: {str(e)}")
            return []

    async def update(
            self, collection: str, id: str, update_data: Dict[str, Any]
    ) -> bool:
        try:
            result = await db[collection].update_one({"_id": id}, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            log_error(f"Database update error: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Database update error: {str(e)}"
            )

    async def delete(self, collection: str, id: str) -> bool:
        try:
            result = await db[collection].delete_one({"_id": id})
            return result.deleted_count > 0
        except Exception as e:
            log_error(f"Database delete error: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Database delete error: {str(e)}"
            )
