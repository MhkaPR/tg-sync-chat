from abc import ABC, abstractmethod
from ast import Tuple
from ctypes import Union
from uuid import UUID


class BaseMapperDB(ABC):
    
    @abstractmethod
    @staticmethod
    def get_by_tg_id(tg_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass

    @abstractmethod
    @staticmethod
    def get_by_source_id(source_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass    

    @abstractmethod
    @staticmethod
    def set(tg_id: Union[int, UUID], source_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass

    @abstractmethod
    @staticmethod
    def delete(source_id:Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass 


