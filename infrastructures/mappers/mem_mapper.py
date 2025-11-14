from typing import Union, Tuple, Optional
from uuid import UUID
from interfaces.mapper import BaseMapperDB

class MemoryMapperDB(BaseMapperDB):
    """
    Async in-memory implementation of BaseMapperDB.
    Stores mapping between Telegram IDs and source IDs.
    """

    def __init__(self):
        # key: tg_id, value: source_id
        self._storage: dict[Union[int, UUID], Union[int, UUID]] = {}

    async def get_by_tg_id(self, tg_id: Union[int, UUID]) -> Optional[Tuple[Union[int, UUID], Union[int, UUID]]]:
        """Get the source_id by Telegram ID."""
        source_id = self._storage.get(tg_id)
        if source_id is not None:
            return tg_id, source_id
        return None

    async def get_by_source_id(self, source_id: Union[int, UUID]) -> Optional[Tuple[Union[int, UUID], Union[int, UUID]]]:
        """Get the Telegram ID by source ID."""
        for tg_id, src_id in self._storage.items():
            if src_id == source_id:
                return tg_id, src_id
        return None

    async def set(self, tg_id: Union[int, UUID], source_id: Union[int, UUID]) -> Tuple[Union[int, UUID], Union[int, UUID]]:
        """Set a mapping between Telegram ID and source ID."""
        self._storage[tg_id] = source_id
        return tg_id, source_id

    async def delete(self, source_id: Union[int, UUID]) -> Optional[Tuple[Union[int, UUID], Union[int, UUID]]]:
        """Delete mapping by source ID."""
        for tg_id, src_id in list(self._storage.items()):
            if src_id == source_id:
                del self._storage[tg_id]
                return tg_id, src_id
        return None
