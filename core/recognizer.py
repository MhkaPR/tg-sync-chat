from typing import List
from DTOs.repo_dtos import MessageDTO
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

    async def find_creatables(self) -> List[MessageDTO]:
        creatables = []
        for obj in self.truth_repo.all():
            try:
                await self.mapper.get_telegram_id(obj.id)
            except ObjNotFount:
                creatables.append(obj)
        return creatables
    
    async def find_updatables(self)-> List[MessageDTO]:
        updateables = []
        for obj in self.truth_repo.all():
            try:
                tg_id = await self.mapper.get_telegram_id(source_id=obj.id)
            except ObjNotFount:
                tg_id = None
            tg_obj = self.tg_repo.load(id=tg_id)
            if tg_id and tg_obj.message == obj.message:
                updateables.append(obj)
        return updateables
    
    async def find_deletables(self) -> List[MessageDTO]:
        deletables = []
        for obj in self.tg_repo.load_all():
            try:
                await self.mapper.get_source_id(tg_id=obj.id)
            except ObjNotFount:
                deletables.append(obj)
        return deletables
