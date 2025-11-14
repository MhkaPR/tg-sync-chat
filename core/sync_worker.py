from typing import List
from core.mapper import Mapper
from interfaces.tg_repository import BaseTgRepo
from interfaces.truth_repository import BaseTruthRepo


class SyncWorker:
    def __init__(self, mapper: Mapper, truth_repo: BaseTruthRepo, tg_repo: BaseTgRepo):
        self.mapper = mapper
        self.truth_repo  = truth_repo
        self.tg_repo = tg_repo

        self.creatables: List[dict] = []
        self.updatables: List[dict] = []
        self.deletables: List[dict] = []

    async def load_available_changes(
            self,
            creatables: List[dict],
            updatables: List[dict],
            deletables: List[dict]
        ) -> None:

        self.creatables = creatables
        self.updatables = updatables
        self.deletables = deletables

    async def synchronize(self, also_deletables: bool = False):
        await self.sync_creatables()
        await self.sync_updatables()
        if also_deletables:
            await self.sync_deletables()

    async def sync_creatables(self) -> None:
        for obj in self.creatables:
            tg_obj = {
                "sync_data": obj["sync_data"]
            }
            tg_obj = await self.tg_repo.create(tg_obj)
            await self.mapper.save_mapping(obj["id"], tg_id=tg_obj["id"])

    async def sync_updatables(self) -> None:
        for obj in self.updatables:
            tg_obj = {
                "id": self.mapper.get_telegram_id(obj["id"]),
                "sync_data": obj["sync_data"]
            }
            await self.tg_repo.update(tg_obj)

    async def sync_deletables(self) -> None:
        for tg_obj in self.deletables:
            await self.tg_repo.delete(tg_obj["id"])
