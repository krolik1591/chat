from pprint import pprint

from peewee import fn, JOIN

from bot.db import first_start
from bot.db.db import Balance, User, Token, Transactions, GameLog


async def tabl1():
    res = await GameLog.select(
        fn.DATE(GameLog.timestamp).alias('date'),
        GameLog.token_id,
        fn.SUM(GameLog.result).alias('total_win'),
        fn.SUM(GameLog.bet).alias('total_bet'),
        fn.GROUP_CONCAT(fn.DISTINCT(GameLog.user_id)).alias('users_id'),
        fn.GROUP_CONCAT(fn.DISTINCT(User.username)).alias('users')
    ).join(User, on=(User.user_id == GameLog.user_id)) \
        .group_by(fn.DATE(GameLog.timestamp), GameLog.token_id).dicts()

    # todo total_bet - total_win

    return res


async def tabl2():
    result = await User.select(
        User.user_id, User.username, User.timestamp_registered, GameLog.token_id,
        fn.Sum(GameLog.result).alias('total_win'),
        fn.Sum(GameLog.bet).alias('total_lose'),
        Balance.amount
    ) \
        .join(GameLog, JOIN.INNER, on=(User.user_id == GameLog.user_id)).switch(GameLog) \
        .join(Balance, JOIN.LEFT_OUTER,
              on=((Balance.user_id == GameLog.user_id) & (Balance.token_id == GameLog.token_id))) \
        .group_by(GameLog.user_id, GameLog.token_id).dicts()

    # todo total_bet - total_win


    return result


if __name__ == "__main__":
    async def test():
        await first_start()
        res = await tabl2()
        pprint(res)


    import asyncio

    asyncio.run(test())
