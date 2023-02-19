from datetime import datetime

from peewee import fn

from bot.db import first_start
from bot.db.db import Balances, User, Token, Transactions, GameLogs


async def create_new_user(tg_id):
    return await User.create(tg_id=tg_id, timestamp_registered=datetime.utcnow(),
                             timestamp_last_active=datetime.utcnow())


async def add_new_transaction(user_id, token_id, is_deposit, logical_time, amount, tx_address, tx_hash):
    return await Transactions.create(user_id=user_id, token_id=token_id, is_deposit=is_deposit,
                                     logical_time=logical_time, amount=amount,
                                     tx_address=tx_address, tx_hash=tx_hash)


async def get_user_balances(user_id):
    return await Balances.select(Balances.amount, Token.icon, Token.price, User.lang) \
        .join(Token).switch(Balances) \
        .join(User) \
        .where(Balances.user_id == user_id)


async def get_last_transaction(tg_id, token_id):
    return await Transactions.select(Transactions.tx_hash, fn.Max(Transactions.logical_time)) \
        .where(Transactions.user_id == tg_id, Transactions.token_id == token_id)


async def get_user_lang(tg_id):
    user_lang = await User.select(User.lang).where(User.tg_id == tg_id)
    return user_lang[0].lang


async def set_user_lang(tg_id, new_lang):
    return await User.update({User.lang: new_lang}).where(User.tg_id == tg_id)


async def set_user_last_active(tg_id):
    return await User.update({User.timestamp_last_active: datetime.utcnow()}).where(User.tg_id == tg_id)


async def insert_game_log(user_id, token_id, game_info, bet, result, game):
    return await GameLogs.create(user_id=user_id, token_id=token_id, game_info=game_info,
                                 bet=bet, result=result, timestamp=datetime.utcnow(), game=game)


if __name__ == "__main__":

    async def test():
        await first_start()
        # for i in await get_last_transaction(2, 'demo'):
        #     print(i.tx_hash, i.logical_time)
        # print(await get_last_transaction(1, 'ton'))
        # await create_new_user(2)
        # await set_user_lang(1, 'ua')
        # print(await get_user_lang(1))
        # await set_user_last_active(1)
        # await insert_game_log(3, 'demo', 'PEREMOGA', 33, 1, 'EQAwmioWn9M2qqbtUPjPFY50-0NENZFL2D5Kr_xu8nG5Qswm')
        # print(await get_last_transaction(3))
        # await add_new_transaction(1, 'ton', 32, 1488, 53,
        #                           'kar',
        #                           'poop')
        # hui = await get_user_balances(3)
        # for i in hui:
        #     print(i.token.icon, i.amount, i.user.lang)


    import asyncio

    asyncio.run(test())
