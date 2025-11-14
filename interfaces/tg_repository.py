from abc import ABC, abstractmethod
from typing import List, Union
import uuid


class BaseTgRepo(ABC):

    @abstractmethod
    def create(self, data: dict) -> dict:
        pass

    @abstractmethod
    def update(self, data: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, tg_id: int) -> None:
        pass

    @abstractmethod
    def store(self, msg_object):
        pass

    @abstractmethod
    def load(self, id):
        pass

    @abstractmethod
    def load_all(self, ):
        pass
