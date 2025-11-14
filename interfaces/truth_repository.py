from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTruthRepo(ABC):
    
    @abstractmethod
    def get_by_id(id: Union[int, uuid.UUID]) -> dict:
        pass

    @abstractmethod
    def filter(**fields) -> List[dict]:
        pass

    @abstractmethod
    def all() -> List[dict]:
        pass

    @abstractmethod
    def create(data: dict) -> dict:
        pass

    @abstractmethod
    def update(data: dict) -> dict:
        pass

    @abstractmethod
    def delete(id:Union[int, uuid.UUID]) -> None:
        pass
