import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from bot.utils.config_reader import config
from bot.handlers import default_commands, spin
from bot.middlewares.throttling import ThrottlingMiddleware


async def main():
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(url=config.redis, connection_kwargs={"decode_responses": True})
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    dp.message.filter(F.chat.type == "private")  # only private chats allowed

    dp.include_router(default_commands.router)
    dp.include_router(spin.router)

    dp.message.middleware(ThrottlingMiddleware())

    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="Перезапустить казино"),
    ], scope=types.BotCommandScopeAllPrivateChats())


if __name__ == '__main__':
    asyncio.run(main())
