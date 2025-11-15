import pytest
from uuid import uuid4
from DTOs.repo_dtos import MessageDTO
from infrastructures.repositories.mem_truth_repo import MemoryTruthRepo

def test_memory_truth_repo_crud():
    repo = MemoryTruthRepo

    # Create
    msg = MessageDTO(id=None, message="test", extra_data={})
    created = repo.create(msg)
    assert created.id is not None
    assert repo.get_by_id(created.id).message == "test"

    # Update
    created.message = "updated"
    updated = repo.update(created)
    assert updated.message == "updated"

    # Update non-existent
    msg2 = MessageDTO(id=uuid4(), message="nonexist", extra_data={})
    with pytest.raises(ValueError):
        repo.update(msg2)

    # All
    all_records = repo.all()
    assert updated in all_records

    # Delete
    repo.delete(created.id)
    assert repo.get_by_id(created.id) is None
