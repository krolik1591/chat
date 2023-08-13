import json
import time

from peewee import fn

from bot.db.models import GameLog, Promocodes, User


# users

async def add_new_user(user_id, username=None):
    return await User.create(user_id=user_id, timestamp_registered=time.time(), username=username)


async def is_user_exists(user_id):
    return await User.select().where(User.user_id == user_id).exists()


# games

async def add_game_result(user_id, game, result):
    return await GameLog.create(user_id=user_id, game=game, result=result, timestamp=time.time())


# promocodes

async def create_new_promo(admin_id, promo_name):
    return await Promocodes.create(promo_name=promo_name, who_create=admin_id, timestamp_registered=time.time())


async def add_new_promo_to_user(user_id, promo_name):
    active_promos = await get_user_promos(user_id)
    if active_promos is None:
        active_promos = []
    else:
        active_promos = json.loads(active_promos)

    active_promos.append(promo_name)
    json_promos = json.dumps(active_promos)

    return await User.update(active_promos=json_promos).where(User.user_id == user_id)


async def is_promo_in_db(promo_name):
    return await Promocodes.select().where(Promocodes.promo_name == promo_name).exists()


async def get_all_promos():
    return await Promocodes.select(Promocodes.promo_name).scalars()


async def get_user_promos(user_id):
    result = await User.select(User.active_promos).where(User.user_id == user_id).scalars()
    if result[0] is None:
        return None
    return result[0]


async def get_available_user_promo(user_id):
    exist_promos = await get_all_promos()
    active_user_promos = await get_user_promos(user_id)
    available_promo = list(set(exist_promos).difference(active_user_promos))
    return available_promo


if __name__ == "__main__":
    import asyncio

    async def test():
        # x = await get_user_promos(357108179)
        x = await add_new_promo_to_user(357108179, ' 152')
        print(x, type(x))

    asyncio.run(test())
