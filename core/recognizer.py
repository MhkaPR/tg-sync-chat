from typing import List
from core import mapper
from core.mapper import Mapper
from exceptions.repositories import ObjNotFount
from interfaces.tg_repository import BaseTgRepo
from interfaces.truth_repository import BaseTruthRepo


class Recognizer:
    
    def __init__(self, mapper: Mapper, truth_repo: BaseTruthRepo, tg_repo: BaseTgRepo):
        self.mapper = mapper
        self.truth_repo = truth_repo
        self.tg_repo = tg_repo

    async def find_creatables(self) -> List[dict]:
        creatables = []
        for obj in self.truth_repo.all():
            try:
                await self.mapper.get_telegram_id(obj["id"])
            except ObjNotFount:
                creatables.append(obj)
        return creatables
    
    async def find_updatables(self)-> List[dict]:
        updateables = []
        for obj in self.truth_repo.all():
            tg_id =await self.mapper.get_telegram_id(obj["id"])
            tg_obj =await self.tg_repo.load(tg_id=tg_id)
            if tg_obj["sync_data"] == obj["sync_data"]:
                updateables.append(obj)
        return updateables
    
    async def find_deletables(self) -> List[dict]:
        deletables = []
        for obj in self.tg_repo.load_all():
            try:
                await self.mapper.get_source_id(tg_id=obj["id"])
            except ObjNotFount:
                deletables.append(obj)
        return deletables
