from typing import List
from DTOs.repo_dtos import MessageDTO
from core.mapper import Mapper
from interfaces.tg_repository import BaseTgRepo
from interfaces.truth_repository import BaseTruthRepo


class SyncWorker:
    def __init__(self, mapper: Mapper, truth_repo: BaseTruthRepo, tg_repo: BaseTgRepo):
        self.mapper = mapper
        self.truth_repo  = truth_repo
        self.tg_repo = tg_repo

        self.creatables: List[MessageDTO] = []
        self.updatables: List[MessageDTO] = []
        self.deletables: List[MessageDTO] = []

    def load_available_changes(
            self,
            creatables: List[MessageDTO],
            updatables: List[MessageDTO],
            deletables: List[MessageDTO]
        ) -> None:

        self.creatables = creatables.copy()
        self.updatables = updatables.copy()
        self.deletables = deletables.copy()

    async def synchronize(self, also_deletables: bool = False):
        s_creatables = self.sync_creatables()
        s_updatables = self.sync_updatables()
        if also_deletables:
            await self.sync_deletables()
        await s_creatables
        await s_updatables

    async def sync_creatables(self) -> None:
        for obj in self.creatables:
            tg_obj = MessageDTO(id=None, message=obj.message, extra_data={})
            tg_obj = await self.tg_repo.create(tg_obj)
            await self.mapper.save_mapping(source_id=obj.id, tg_id=tg_obj.id)

    async def sync_updatables(self) -> None:
        for obj in self.updatables:
            tg_obj = MessageDTO(id=await self.mapper.get_telegram_id(obj.id), message=obj.message, extra_data={})
            await self.tg_repo.update(tg_obj)

    async def sync_deletables(self) -> None:
        for tg_obj in self.deletables:
           await self.tg_repo.delete(tg_obj.id)
