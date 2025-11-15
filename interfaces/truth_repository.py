from abc import ABC, abstractmethod
from typing import List, Union
import uuid
from DTOs.repo_dtos import MessageDTO


class BaseTruthRepo(ABC):
    
    @abstractmethod
    def get_by_id(id: Union[int, uuid.UUID]) -> MessageDTO:
        pass

    @abstractmethod
    def filter(**fields) -> List[MessageDTO]:
        pass

    @abstractmethod
    def all() -> List[MessageDTO]:
        pass

    @abstractmethod
    def create(data: MessageDTO) -> MessageDTO:
        pass

    @abstractmethod
    def update(data: MessageDTO) -> MessageDTO:
        pass

    @abstractmethod
    def delete(id:Union[int, uuid.UUID]) -> None:
        pass
