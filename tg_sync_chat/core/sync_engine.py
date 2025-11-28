from asyncio import sleep
from asyncio.log import logger
from core.mapper import Mapper
from core.recognizer import Recognizer
from core.sync_worker import SyncWorker
from infrastructures.mappers.mem_mapper import MemoryMapperDB
from infrastructures.repositories.aiogram import AiogramMemoryRepo
from infrastructures.repositories.mem_truth_repo import MemoryTruthRepo
from interfaces.tg_repository import BaseTgRepo
from interfaces.truth_repository import BaseTruthRepo


class SyncEngine:

    def __init__(
            self, mapper: Mapper = None,
            truth_repo: BaseTruthRepo= None,
            telegram_repo: BaseTgRepo = None,
            recognizer: Recognizer = None, 
            sync_worker: SyncWorker = None,
            duration = 1,
            **kwargs
            ):
        self.mapper = Mapper(MemoryMapperDB()) if not mapper else mapper
        self.truth_repo = MemoryTruthRepo() if not truth_repo else truth_repo
        self.telegram_repo = AiogramMemoryRepo(kwargs["bot"], kwargs["channel_id"]) if not telegram_repo else telegram_repo
        self.recognizer = Recognizer(self.mapper, self.truth_repo, self.telegram_repo) if not recognizer else recognizer
        self.sync_worker = SyncWorker(self.mapper, self.truth_repo, self.telegram_repo) if not sync_worker else sync_worker
        self._duration = duration
        self._stop = False

        self._ignored_exceptions = [*kwargs.get("ignored_exceptions", [])]

    async def run(self, also_deletables = False):
        while not self._stop:
            try:
                creatables =await self.recognizer.find_creatables()
                updatables =await self.recognizer.find_updatables()
                deletables = []
                if also_deletables: 
                    deletables =await self.recognizer.find_deletables()
                
                self.sync_worker.load_available_changes(
                    creatables=creatables,
                    updatables=updatables,
                    deletables=deletables
                )
                self.sync_worker.synchronize(also_deletables=also_deletables)
            except Exception as e:
                if type(e) not in self._ignored_exceptions:
                    raise e
                logger.error(f"An error happens with type of {type(e)}",extra={"error": e})
            await sleep(self._duration)

    async def stop(self):
        self._stop = True

    
                