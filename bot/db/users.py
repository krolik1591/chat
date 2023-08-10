import time

from peewee import fn

from bot.db.models import GameLog, User


# users

async def add_new_user(user_id, username=None):
    return await User.create(user_id=user_id, timestamp_registered=time.time(), username=username)


async def is_user_exists(user_id):
    return await User.select().where(User.user_id == user_id).exists()


# games

async def add_game_result(user_id, game, result):
    return await GameLog.create(user_id=user_id, game=game, result=result, timestamp=time.time())


if __name__ == "__main__":
    import asyncio

    async def test():
        x = await is_user_exists(3571028179)
        print(x)

    asyncio.run(test())
