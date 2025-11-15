import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from DTOs.repo_dtos import MessageDTO
from core.mapper import Mapper
from core.recognizer import Recognizer
from exceptions.repositories import ObjNotFount

@pytest.mark.asyncio
async def test_recognizer_creatables_updatables_deletables():
    # Setup in-memory repos
    class MockTruthRepo:
        def __init__(self):
            self._data = []
        def all(self):
            return self._data
        def add(self, msg: MessageDTO):
            self._data.append(msg)

    class MockTgRepo:
        def __init__(self):
            self._data = {}
        def load(self, id):
            return self._data.get(id)
        def load_all(self):
            return list(self._data.values())
        def store(self, msg: MessageDTO):
            self._data[msg.id] = msg
            return msg

    truth_repo = MockTruthRepo()
    tg_repo = MockTgRepo()
    mapper = Mapper(AsyncMock())  # AsyncMock mapper

    # Prepare messages
    msg1 = MessageDTO(id=uuid4(), message="Hello", extra_data={})
    msg2 = MessageDTO(id=uuid4(), message="World", extra_data={})
    truth_repo.add(msg1)
    truth_repo.add(msg2)

    # Store one msg in TG repo to simulate existing mapping
    tg_msg = MessageDTO(id=100, message="Hello", extra_data={})
    tg_repo.store(tg_msg)

    # Mock mapper behavior
    mapper.get_telegram_id = AsyncMock(side_effect=lambda x: 100 if x==msg1.id else  ObjNotFount)
    mapper.get_source_id = AsyncMock(side_effect=ObjNotFount)

    recognizer = Recognizer(mapper, truth_repo, tg_repo)

    # Creatables → only msg2 (no mapping yet)
    creatables = await recognizer.find_creatables()
    assert creatables == [msg2]

    # Updatables → msg1 should be updateable (message matches TG repo)
    updatables = await recognizer.find_updatables()
    assert updatables == [msg1]

    # Deletables → tg_msg has no source mapping, so deletable
    deletables = await recognizer.find_deletables()
    assert deletables == [tg_msg]
