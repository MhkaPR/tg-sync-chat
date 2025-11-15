import pytest
from unittest.mock import AsyncMock
from DTOs.repo_dtos import MessageDTO
from infrastructures.repositories.aiogram import AiogramMemoryRepo, DTOAiogramMapper

@pytest.mark.asyncio
async def test_aiogram_memory_repo_create_update_delete_store_load():
    # Mock bot
    mock_bot = AsyncMock()
    mock_bot.send_message.return_value = AsyncMock(message_id=1, text="hello", model_dump=lambda: {"text": "hello"})
    mock_bot.edit_message_text.return_value = AsyncMock(message_id=1, text="updated", model_dump=lambda: {"text": "updated"})
    
    repo = AiogramMemoryRepo(bot=mock_bot, channel_id=123)

    msg_dto = MessageDTO(id=1, message="hello", extra_data={})
    
    # Create
    created = await repo.create(msg_dto)
    assert created.message == "hello"
    assert 1 in repo._storage

    # Update
    msg_dto.message = "updated"
    updated = await repo.update(msg_dto)
    assert updated.message == "updated"

    # Delete
    await repo.delete(1)
    assert 1 not in repo._storage

    # Store & Load
    repo.store(msg_dto)
    loaded = repo.load(1)
    assert loaded == msg_dto

    # Load all
    all_msgs = repo.load_all()
    assert msg_dto in all_msgs
