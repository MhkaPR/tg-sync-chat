from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTruthRepo(ABC):
    
    @abstractmethod
    @staticmethod
    def get_by_id(id: Union[int, uuid.UUID]) -> dict:
        pass

    @abstractmethod
    @staticmethod
    def filter(**fields) -> List[dict]:
        pass

    @abstractmethod
    @staticmethod
    def all() -> List[dict]:
        pass

    @abstractmethod
    @staticmethod
    def create(data: dict) -> dict:
        pass

    @abstractmethod
    @staticmethod
    def update(data: dict) -> dict:
        pass

    @abstractmethod
    @staticmethod
    def delete(id:Union[int, uuid.UUID]) -> None:
        pass
