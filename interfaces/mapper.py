from abc import ABC, abstractmethod
from typing import Tuple
from typing import Union
from uuid import UUID


class BaseMapperDB(ABC):
    
    @abstractmethod
    def get_by_tg_id(tg_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass

    @abstractmethod
    def get_by_source_id(source_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass    

    @abstractmethod
    def set(tg_id: Union[int, UUID], source_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass

    @abstractmethod
    def delete(source_id:Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        pass 


