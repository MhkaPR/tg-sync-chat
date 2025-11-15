import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from DTOs.repo_dtos import MessageDTO
from core.mapper import Mapper
from core.sync_worker import SyncWorker

@pytest.mark.asyncio
async def test_syncworker_synchronize_creatables_updatables_deletables():
    # Setup mocks
    tg_repo = AsyncMock()
    mapper = AsyncMock()
    worker = SyncWorker(mapper=mapper, truth_repo=None, tg_repo=tg_repo)

    # Prepare test messages
    msg1 = MessageDTO(id=uuid4(), message="CreateMe", extra_data={})
    msg2 = MessageDTO(id=uuid4(), message="UpdateMe", extra_data={})
    msg3 = MessageDTO(id=uuid4(), message="DeleteMe", extra_data={})

    # Load available changes
    worker.load_available_changes(
        creatables=[msg1],
        updatables=[msg2],
        deletables=[msg3]
    )

    # Run synchronize with deletables
    await worker.synchronize(also_deletables=True)

    # Check that tg_repo.create called for creatables
    tg_repo.create.assert_called_with(MessageDTO(id=None, message=msg1.message, extra_data={}))
    # Check that tg_repo.update called for updatables
    tg_repo.update.assert_called_with(MessageDTO(id=await mapper.get_telegram_id(msg2.id), message=msg2.message, extra_data={}))
    # Check that tg_repo.delete called for deletables
    tg_repo.delete.assert_called_with(msg3.id)

@pytest.mark.asyncio
async def test_syncworker_sync_creatables_and_updatables():
    # Minimal mocks to test individual methods
    tg_repo = AsyncMock()
    mapper = AsyncMock()
    worker = SyncWorker(mapper=mapper, truth_repo=None, tg_repo=tg_repo)

    msg1 = MessageDTO(id=uuid4(), message="Create", extra_data={})
    msg2 = MessageDTO(id=uuid4(), message="Update", extra_data={})

    worker.creatables = [msg1]
    worker.updatables = [msg2]

    await worker.sync_creatables()
    await worker.sync_updatables()

    # mapper.save_mapping called for creatables
    mapper.save_mapping.assert_called()
    # tg_repo.update called for updatables
    tg_repo.update.assert_called()
