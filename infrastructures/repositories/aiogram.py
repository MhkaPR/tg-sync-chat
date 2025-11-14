from os import wait
from typing import Dict, List, Optional
from aiogram import Bot
from aiogram.types import Message
from interfaces.tg_repository import BaseTgRepo

class AiogramChannelRepo(BaseTgRepo):
    """Telegram repository using Aiogram v3."""

    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self._cache: Dict[int, dict] = {}  # store messages as dict

    async def _fetch_history(self, limit: int = 100) -> None:
        """Fetch recent messages from the channel and store in cache."""
        offset_id = 0
        while True:
            history: List[Message] =await self.bot.get_chat_history(
                chat_id=self.channel_id, limit=limit, offset_id=offset_id
            )
            if not history:
                break
            for msg in history:
                self._cache[msg.message_id] = msg.model_dump()
            offset_id = min(msg.message_id for msg in history) - 1
            if len(history) < limit:
                break

    async def get_by_id(self, tg_id: int) -> Optional[dict]:
        if tg_id not in self._cache:
            await self._fetch_history()
        return self._cache.get(tg_id)

    async def all(self) -> List[dict]:
        await self._fetch_history()
        return list(self._cache.values())

    async def filter(self, **fields) -> List[dict]:
        await self._fetch_history()
        results = []
        for msg in self._cache.values():
            if all(msg.get(k) == v for k, v in fields.items()):
                results.append(msg)
        return results

    async def create(self, data: dict) -> dict:
        text = data.get("sync_data", "")
        msg: Message = await self.bot.send_message(chat_id=self.channel_id, text=text)
        self._cache[msg.message_id] = msg.model_dump()
        return self._cache[msg.message_id]

    async def update(self, data: dict) -> dict:
        tg_id = data.get("id")
        text = data.get("sync_data", "")
        msg: Message = await self.bot.edit_message_text(
            chat_id=self.channel_id,
            message_id=tg_id,
            text=text
        )
        self._cache[tg_id] = msg.model_dump()
        return self._cache[tg_id]

    async def delete(self, tg_id: int) -> None:
        await self.bot.delete_message(chat_id=self.channel_id, message_id=tg_id)
        self._cache.pop(tg_id, None)
