import uuid
from typing import List, Union
from interfaces.truth_repository import BaseTruthRepo

class MemoryTruthRepo(BaseTruthRepo):
    """
    In-memory implementation of BaseTruthRepo.
    Acts as the source of truth repository.
    """

    _storage: dict[Union[int, uuid.UUID], dict] = {}

    @staticmethod
    def get_by_id(id: Union[int, uuid.UUID]) -> dict:
        """Get a record by ID."""
        return MemoryTruthRepo._storage.get(id)

    @staticmethod
    def filter(**fields) -> List[dict]:
        """Return all records that match the given fields."""
        results = []
        for record in MemoryTruthRepo._storage.values():
            if all(record.get(k) == v for k, v in fields.items()):
                results.append(record)
        return results

    @staticmethod
    def all() -> List[dict]:
        """Return all records."""
        return list(MemoryTruthRepo._storage.values())

    @staticmethod
    def create(data: dict) -> dict:
        """Create a new record. Generates a UUID if no ID provided."""
        record_id = data.get("id") or uuid.uuid4()
        data["id"] = record_id
        MemoryTruthRepo._storage[record_id] = data
        return data

    @staticmethod
    def update(data: dict) -> dict:
        """Update an existing record by ID."""
        record_id = data.get("id")
        if record_id in MemoryTruthRepo._storage:
            MemoryTruthRepo._storage[record_id].update(data)
            return MemoryTruthRepo._storage[record_id]
        else:
            raise ValueError(f"Record with ID {record_id} not found")

    @staticmethod
    def delete(id: Union[int, uuid.UUID]) -> None:
        """Delete a record by ID."""
        if id in MemoryTruthRepo._storage:
            del MemoryTruthRepo._storage[id]
