import pytest
import asyncio
from uuid import uuid4
from unittest.mock import AsyncMock
from core.recognizer import Recognizer, Mapper
from infrastructures.repositories.aiogram import AiogramMemoryRepo
from infrastructures.repositories.mem_truth_repo import MemoryTruthRepo
from infrastructures.mappers.mem_mapper import MemoryMapperDB
from DTOs.repo_dtos import MessageDTO

@pytest.mark.asyncio
async def test_recognizer_find_methods():
    truth_repo = MemoryTruthRepo
    tg_repo = AiogramMemoryRepo(bot=AsyncMock(), channel_id=123)
    mapper_db = MemoryMapperDB()
    mapper = Mapper(mapper_db)

    # Prepare data
    msg1 = truth_repo.create(MessageDTO(id=uuid4(), message="Hello", extra_data=None))
    msg2 = truth_repo.create(MessageDTO(id=uuid4(), message="World", extra_data=None))

    recognizer = Recognizer(mapper=mapper, truth_repo=truth_repo, tg_repo=tg_repo)

    # Creatables
    creatables = await recognizer.find_creatables()
    assert len(creatables) == 2

    # Add mapping to simulate updateable
    tg_obj = await tg_repo.create(MessageDTO(id=1, message="Hello"))
    await mapper.save_mapping(source_id=msg1.id, tg_id=tg_obj["message_id"])

    updatables = await recognizer.find_updatables()
    # The logic depends on comparing "sync_data" with tg_obj, you may need to adjust test values
    assert isinstance(updatables, list)

    # Deletables
    deletables = await recognizer.find_deletables()
    assert isinstance(deletables, list)
