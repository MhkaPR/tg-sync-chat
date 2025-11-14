from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTgRepo(ABC):
    
    @abstractmethod
    @staticmethod
    def get_by_id(tg_id: int) -> dict:
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
    def delete(tg_id: int) -> None:
        pass
