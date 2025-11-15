import pytest
from uuid import uuid4
from infrastructures.mappers.mem_mapper import MemoryMapperDB
from exceptions.repositories import ObjNotFount

def test_memory_mapper_db_set_get_delete():
    db = MemoryMapperDB()
    tg_id = 1
    source_id = uuid4()

    # Set
    db.set(tg_id=tg_id, source_id=source_id)
    assert db.get_by_tg_id(tg_id)[1] == source_id
    assert db.get_by_source_id(source_id)[0] == tg_id

    # Delete
    db.delete(source_id)
    with pytest.raises(ObjNotFount):
        db.get_by_source_id(source_id)
    with pytest.raises(ObjNotFount):
        db.get_by_tg_id(tg_id)
