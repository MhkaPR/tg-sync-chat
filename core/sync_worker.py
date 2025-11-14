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

    def load_available_changes(
            self,
            creatables: List[dict],
            updatables: List[dict],
            deletables: List[dict]
        ) -> None:

        self.creatables = creatables
        self.updatables = updatables
        self.deletables = deletables

    def synchronize(self, also_deletables: bool = False):
        self.sync_creatables()
        self.sync_updatables()
        if also_deletables:
            self.sync_deletables()

    def sync_creatables(self) -> None:
        for obj in self.creatables:
            tg_obj = {
                "sync_data": obj["sync_data"]
            }
            tg_obj = self.tg_repo.create(tg_obj)
            self.mapper.save_mapping(obj["id"], tg_id=tg_obj["message_id"])

    def sync_updatables(self) -> None:
        for obj in self.updatables:
            tg_obj = {
                "id": self.mapper.get_telegram_id(obj["id"]),
                "sync_data": obj["sync_data"]
            }
            self.tg_repo.update(tg_obj)

    def sync_deletables(self) -> None:
        for tg_obj in self.deletables:
            self.tg_repo.delete(tg_obj["id"])
