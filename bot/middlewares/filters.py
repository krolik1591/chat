from typing import Any

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from bot.utils.config_reader import config


class FilterChatId(BaseFilter):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    async def __call__(self, message: Message) -> bool:
        return message.chat.id == config.admin_chat_id
