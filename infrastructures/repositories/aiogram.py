from abc import ABC
from typing import List, Dict, Optional
from aiogram import Bot
from aiogram.types import Message
from interfaces.tg_repository import BaseTgRepo

class AiogramChannelRepo(BaseTgRepo):
    """
    A repository that interacts directly with a Telegram channel using Aiogram.
    Supports sending, editing, deleting, and fetching messages.
    """

    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self._cache: Dict[int, dict] = {}  # local cache of messages

    async def _fetch_history(self, limit: int = 100) -> None:
        """Fetch recent messages from the channel and store in cache."""
        offset_id = 0
        while True:
            history = await self.bot.get_chat_history(chat_id=self.channel_id, limit=limit, offset_id=offset_id)
            if not history:
                break
            for msg in history:
                self._cache[msg.message_id] = msg.to_python()
            offset_id = min(msg.message_id for msg in history) - 1
            if len(history) < limit:
                break

    async def get_by_id(self, tg_id: int) -> Optional[dict]:
        """Get a message by Telegram message ID."""
        if tg_id not in self._cache:
            await self._fetch_history()
        return self._cache.get(tg_id)

    async def all(self) -> List[dict]:
        """Return all messages from the channel (using cache)."""
        await self._fetch_history()
        return list(self._cache.values())

    async def filter(self, **fields) -> List[dict]:
        """
        Filter messages by fields (e.g., text='hello').
        Fetches messages from channel if not cached.
        """
        await self._fetch_history()
        results = []
        for msg in self._cache.values():
            if all(msg.get(k) == v for k, v in fields.items()):
                results.append(msg)
        return results

    async def create(self, data: dict) -> dict:
        """Send a new message to the channel."""
        text = data.get("text", "")
        msg: Message = await self.bot.send_message(chat_id=self.channel_id, text=text)
        self._cache[msg.message_id] = msg.to_python()
        return msg.to_python()

    async def update(self, data: dict) -> dict:
        """Edit an existing message in the channel."""
        tg_id = data.get("tg_id")
        text = data.get("text", "")
        msg: Message = await self.bot.edit_message_text(chat_id=self.channel_id, message_id=tg_id, text=text)
        self._cache[tg_id] = msg.to_python()
        return msg.to_python()

    async def delete(self, tg_id: int) -> None:
        """Delete a message from the channel."""
        await self.bot.delete_message(chat_id=self.channel_id, message_id=tg_id)
        if tg_id in self._cache:
            del self._cache[tg_id]
