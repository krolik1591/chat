from pprint import pprint

from peewee import fn, JOIN

from bot.db import first_start
from bot.db.db import Balances, User, Token, Transactions, GameLogs


async def tabl1():
    res = await GameLogs.select(
        fn.DATE(GameLogs.timestamp).alias('date'),
        GameLogs.token_id,
        fn.SUM(GameLogs.result).alias('total_win'),
        fn.SUM(GameLogs.bet).alias('total_bet'),
        fn.GROUP_CONCAT(fn.DISTINCT(GameLogs.user_id)).alias('users_id'),
        fn.GROUP_CONCAT(fn.DISTINCT(User.username)).alias('users')
    ).join(User, on=(User.user_id == GameLogs.user_id)) \
        .group_by(fn.DATE(GameLogs.timestamp), GameLogs.token_id).dicts()

    # todo total_bet - total_win

    return res


async def tabl2():
    result = await User.select(
        User.user_id, User.username, User.timestamp_registered, GameLogs.token_id,
        fn.Sum(GameLogs.result).alias('total_win'),
        fn.Sum(GameLogs.bet).alias('total_lose'),
        Balances.amount
    ) \
        .join(GameLogs, JOIN.INNER, on=(User.user_id == GameLogs.user_id)).switch(GameLogs) \
        .join(Balances, JOIN.LEFT_OUTER,
              on=((Balances.user_id == GameLogs.user_id) & (Balances.token_id == GameLogs.token_id))) \
        .group_by(GameLogs.user_id, GameLogs.token_id).dicts()

    # todo total_bet - total_win


    return result


if __name__ == "__main__":
    async def test():
        await first_start()
        res = await tabl2()
        pprint(res)


    import asyncio

    asyncio.run(test())
