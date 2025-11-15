from ctypes import Union
from os import wait
from typing import Dict, List, Optional
import uuid
from aiogram import Bot
from aiogram.types import Message
from DTOs.repo_dtos import MessageDTO
from interfaces.tg_repository import BaseTgRepo

class DTOAiogramMapper:
    @staticmethod
    def to_dto(msg: Message):
        return MessageDTO(msg.message_id, msg.text, msg.model_dump())


class AiogramMemoryRepo(BaseTgRepo):

    dto_mapper = DTOAiogramMapper

    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self._storage: Dict[int, MessageDTO] = {}

    
    async def create(self, data: MessageDTO) -> MessageDTO:
        text = data.message
        msg: Message = await self.bot.send_message(chat_id=self.channel_id, text=text)
        self._storage[msg.message_id] = self.dto_mapper.to_dto(msg)
        return self._storage[msg.message_id]

    async def update(self, data: MessageDTO) -> MessageDTO:
        tg_id = data.id
        text = data.message
        msg: Message = await self.bot.edit_message_text(
            chat_id=self.channel_id,
            message_id=tg_id,
            text=text
        )
        self._storage[tg_id] = self.dto_mapper.to_dto(msg)
        return self._storage[tg_id]

    async def delete(self, tg_id: int) -> None:
        await self.bot.delete_message(chat_id=self.channel_id, message_id=tg_id)
        self._storage.pop(tg_id, None)


    def store(self, msg_object: MessageDTO) -> MessageDTO:
        self._storage[msg_object.id] = msg_object
        return msg_object
    def load(self, id: Union[int , uuid.UUID]) -> MessageDTO:
        return self._storage.get(id)
    
    def load_all(self) -> List[MessageDTO]:
        return list(self._storage.values())
    