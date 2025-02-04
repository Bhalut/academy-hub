"""
Module that defines the base interface for data repositories.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class BaseRepository(ABC):
    """
    Abstract class that defines basic CRUD operations for a repository.
    """

    @abstractmethod
    async def insert(self, collection: str, data: Dict[str, Any]) -> bool:
        """
        Inserts a record into the specified collection.

        Args:
            collection (str): Name of the collection.
            data (Dict[str, Any]): Data to insert.

        Returns:
            bool: True if the insert was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def find_by_id(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        """
        Searches for a record by its id.

        Args:
            collection (str): Name of the collection.
            id (str): Record identifier.

        Returns:
            Optional[Dict[str, Any]]: Record data if found, otherwise None.
        """
        pass

    @abstractmethod
    async def find_all(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Finds all records that match the provided filters.

        Args:
            collection (str): Name of the collection.
            filters (Dict[str, Any]): Search filters.

        Returns:
            List[Dict[str, Any]]: List of records found.
        """
        pass

    @abstractmethod
    async def update(self, collection: str, id: str, update_data: Dict[str, Any]) -> bool:
        """
        Updates a specific record.

        Args:
            collection (str): Name of the collection.
            id (str): Record identifier.
            update_data (Dict[str, Any]): Data to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def delete(self, collection: str, id: str) -> bool:
        """
        Deletes a record from the collection.

        Args:
            collection (str): Name of the collection.
            id (str): Record identifier.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        pass
