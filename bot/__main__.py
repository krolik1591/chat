import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.db import first_start
from bot.handlers import routers
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.tokens.token_ton import TonWrapper, watch_txs
from bot.tokens.withdraw_timeout_watcher import find_and_reject_lost_tx
from bot.utils.config_reader import config


async def main():
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(url=config.redis, connection_kwargs={"decode_responses": True})
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # dp.message.filter(F.chat.type == "private")  # only private chats allowed

    for router in routers:
        dp.include_router(router)

    i18n_path = Path(__file__).parent.parent / 'locales'
    i18n = I18n(path=i18n_path, default_locale="uk", domain="messages")

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())  # todo check if it works

    dp.update.middleware(FSMI18nMiddleware(i18n))

    await set_bot_commands(bot)

    await first_start()

    ton_wrapper = await TonWrapper.create_archival(master_wallet_mnemon=config.wallet_seed)
    TonWrapper.INSTANCE = ton_wrapper

    asyncio.create_task(watch_txs(ton_wrapper, bot, i18n))
    asyncio.create_task(find_and_reject_lost_tx(bot, i18n))

    try:
        print("me:", await bot.get_me())
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="Перезапустить казино"),
    ], scope=types.BotCommandScopeAllPrivateChats())


if __name__ == '__main__':
    asyncio.run(main())
