from os import wait
from typing import Dict, List, Optional
import uuid
from aiogram import Bot
from aiogram.types import Message
from interfaces.tg_repository import BaseTgRepo

class AiogramMemoryRepo(BaseTgRepo):
    """Telegram repository using Aiogram v3."""
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self._storage: Dict[int, dict] = {}  # store messages as dict

    
    async def create(self, data: dict) -> dict:
        text = data.get("sync_data", "")
        msg: Message = await self.bot.send_message(chat_id=self.channel_id, text=text)
        self._storage[msg.message_id] = msg.model_dump()
        return self._storage[msg.message_id]

    async def update(self, data: dict) -> dict:
        tg_id = data.get("id")
        text = data.get("sync_data", "")
        msg: Message = await self.bot.edit_message_text(
            chat_id=self.channel_id,
            message_id=tg_id,
            text=text
        )
        self._storage[tg_id] = msg.model_dump()
        return self._storage[tg_id]

    async def delete(self, tg_id: int) -> None:
        await self.bot.delete_message(chat_id=self.channel_id, message_id=tg_id)
        self._storage.pop(tg_id, None)


    def store(self, msg_object):
        self._storage[msg_object.message_id] = msg_object

    def load(self, id):
        return self._storage.get(id)
    
    def load_all(self) -> List:
        return list(self._storage.values())