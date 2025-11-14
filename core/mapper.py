from typing import Tuple, Union
from uuid import UUID
from interfaces.mapper import BaseMapperDB
class Mapper:
    def __init__(self, mapper_db: BaseMapperDB, *args, **kwargs):
        self.db = mapper_db

    def save_mapping(self, source_id: Union[int, UUID], tg_id:Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        return self.db.set(tg_id=tg_id, source_id=source_id)

    def get_telegram_id(self, source_id: Union[int , UUID]) -> Union[int, UUID]:
        return self.db.get_by_source_id(source_id=source_id)[0]
    
    def get_source_id(self, tg_id: Union[int, UUID]) -> Union[int, UUID]:
        return self.db.get_by_tg_id(tg_id=tg_id)[1]
    

    def delete_mapping(self, source_id: Union[int, UUID]) -> Tuple[Union[int, UUID]]:
        return self.db.delete(source_id=source_id)