from abc import ABC, abstractmethod
from typing import List, Union
import uuid

from DTOs.repo_dtos import MessageDTO


class BaseTgRepo(ABC):

    @abstractmethod
    def create(self, data: MessageDTO) -> MessageDTO:
        pass

    @abstractmethod
    def update(self, data: MessageDTO) -> MessageDTO:
        pass

    @abstractmethod
    def delete(self, tg_id: Union[int, uuid.UUID]) -> None:
        pass

    @abstractmethod
    def store(self, msg_object: MessageDTO) -> MessageDTO:
        pass

    @abstractmethod
    def load(self, id: Union[int, uuid.UUID]) -> MessageDTO:
        pass

    @abstractmethod
    def load_all(self) -> List[MessageDTO]:
        pass
