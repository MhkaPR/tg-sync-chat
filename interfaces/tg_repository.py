from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTgRepo(ABC):

    @abstractmethod
    def create(data: dict) -> dict:
        pass

    @abstractmethod
    def update(data: dict) -> dict:
        pass

    @abstractmethod
    def delete(tg_id: int) -> None:
        pass

    @abstractmethod
    def store(msg_object):
        pass

    @abstractmethod
    def load(id):
        pass

    @abstractmethod
    def load_all():
        pass
