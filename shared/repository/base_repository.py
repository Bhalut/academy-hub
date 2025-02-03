from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class BaseRepository(ABC):

    @abstractmethod
    async def insert(self, collection: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def find_by_id(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find_all(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def update(self, collection: str, id: str, update_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def delete(self, collection: str, id: str) -> bool:
        pass
