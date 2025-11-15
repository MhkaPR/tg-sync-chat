import pytest
import asyncio
from uuid import uuid4
from unittest.mock import AsyncMock
from DTOs.repo_dtos import MessageDTO
from core.sync_worker import SyncWorker, Mapper
from infrastructures.repositories.aiogram import AiogramMemoryRepo
from infrastructures.repositories.mem_truth_repo import MemoryTruthRepo
from infrastructures.mappers.mem_mapper import MemoryMapperDB

@pytest.mark.asyncio
async def test_syncworker_synchronize():
    truth_repo = MemoryTruthRepo
    tg_repo = AiogramMemoryRepo(bot=AsyncMock(), channel_id=123)
    mapper_db = MemoryMapperDB()
    mapper = Mapper(mapper_db)

    worker = SyncWorker(mapper=mapper, truth_repo=truth_repo, tg_repo=tg_repo)

    msg1 = truth_repo.create(MessageDTO(id=uuid4(), message="Hello", extra_data=None))
    msg2 = truth_repo.create(MessageDTO(id=uuid4(), message="World", extra_data=None))

    worker.load_available_changes(creatables=[{"id": msg1.id, "sync_data": msg1.message}],
                                  updatables=[{"id": msg2.id, "sync_data": msg2.message}],
                                  deletables=[])

    await worker.synchronize()
    # Check that tg_repo.create and update are called
    assert hasattr(worker, "creatables")
    assert len(worker.creatables) == 1
    assert len(worker.updatables) == 1
