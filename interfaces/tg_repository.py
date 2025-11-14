from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTgRepo(ABC):
    
    @abstractmethod
    def get_by_id(tg_id: int) -> dict:
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
    def delete(tg_id: int) -> None:
        pass
