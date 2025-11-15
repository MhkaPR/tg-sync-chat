import pytest
import asyncio
from uuid import uuid4
from core.mapper import Mapper
from infrastructures.mappers.mem_mapper import MemoryMapperDB

@pytest.mark.asyncio
async def test_mapper_save_get_delete():
    mapper_db = MemoryMapperDB()
    mapper = Mapper(mapper_db)
    
    source_id = uuid4()
    tg_id = 100

    # Save mapping
    tg, src = await mapper.save_mapping(source_id=source_id, tg_id=tg_id)
    assert tg == tg_id
    assert src == source_id

    # Get
    assert await mapper.get_telegram_id(source_id) == tg_id
    assert await mapper.get_source_id(tg_id) == source_id

    # Delete
    deleted = await mapper.delete_mapping(source_id)
    assert deleted == (tg_id, source_id)
    # Check not exists
    with pytest.raises(Exception):
        await mapper.get_telegram_id(source_id)
