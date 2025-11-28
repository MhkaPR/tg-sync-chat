import uuid
from typing import List, Union
from DTOs.repo_dtos import MessageDTO
from interfaces.truth_repository import BaseTruthRepo

class MemoryTruthRepo(BaseTruthRepo):
    """
    In-memory implementation of BaseTruthRepo.
    Acts as the source of truth repository.
    """

    _storage: dict[Union[int, uuid.UUID], MessageDTO] = {}

    @staticmethod
    def get_by_id(id: Union[int, uuid.UUID]) -> MessageDTO:
        """Get a record by ID."""
        return MemoryTruthRepo._storage.get(id)

    @staticmethod
    def all() -> List[MessageDTO]:
        """Return all records."""
        return list(MemoryTruthRepo._storage.values())

    @staticmethod
    def create(data: MessageDTO) -> MessageDTO:
        """Create a new record. Generates a UUID if no ID provided."""
        record_id = data.id or uuid.uuid4()
        data.id = record_id
        MemoryTruthRepo._storage[record_id] = data
        return data

    @staticmethod
    def update(data: MessageDTO) -> MessageDTO:
        """Update an existing record by ID."""
        record_id = data.id
        if record_id in MemoryTruthRepo._storage:
            record = MemoryTruthRepo._storage[record_id]
            record.message = data.message
            record.extra_data = record.extra_data
            return MemoryTruthRepo._storage[record_id]
        else:
            raise ValueError(f"Record with ID {record_id} not found")

    @staticmethod
    def delete(id: Union[int, uuid.UUID]) -> None:
        """Delete a record by ID."""
        if id in MemoryTruthRepo._storage:
            del MemoryTruthRepo._storage[id]
