import json
import time
from collections import Counter

from peewee import fn

from bot.db.models import GameLog, Promocodes, User


# users

async def add_new_user(user_id, username):
    if username is None:
        username = ' нема юзернейму'
    return await User.create(user_id=user_id, timestamp_registered=time.time(), username=username)


async def is_user_exists(user_id):
    return await User.select().where(User.user_id == user_id).exists()


async def get_unique_users():
    user_ids = await User.select(User.user_id).distinct()
    return [user_id.user_id for user_id in user_ids]


async def get_username_by_id(user_id):
    result = await User.select().where(User.user_id == user_id)
    return result[0].username


async def update_username(user_id, username):
    if username is None:
        return
    return await User.update({User.username: username}).where(User.user_id == user_id)


# games

async def add_game_result(user_id, game, result):
    return await GameLog.create(user_id=user_id, game=game, result=result, timestamp=time.time())


# promocodes

async def create_new_promo(promo_name, number_of_uses=1):
    return await Promocodes.create(promo_name=promo_name, number_of_uses=number_of_uses, timestamp_registered=time.time())


async def add_new_promo_to_user(user_id, promo_name):
    active_promos = json.loads(await get_user_promos(user_id))
    active_promos.append(promo_name)
    json_promos = json.dumps(active_promos)

    return await User.update(active_promos=json_promos).where(User.user_id == user_id)


async def is_promo_in_db(promo_name):
    return await Promocodes.select().where(Promocodes.promo_name == promo_name).exists()


async def get_all_promos_and_num_of_uses():
    promos = await Promocodes.select(Promocodes)
    result = {promo.promo_name: promo.number_of_uses for promo in promos}
    return result


async def get_user_promos(user_id):
    result = await User.select(User.active_promos).where(User.user_id == user_id).scalars()
    if not result or result[0] is None:
        return json.dumps([])
    return result[0]


async def get_available_user_promo(user_id):
    all_promos_and_uses = await get_all_promos_and_num_of_uses()
    active_user_promos = json.loads(await get_user_promos(user_id))
    promos_count = Counter(active_user_promos)
    for promo_name, count in promos_count.items():
        if count >= all_promos_and_uses[promo_name]:
            all_promos_and_uses.pop(promo_name)
    return [promo_name for promo_name in all_promos_and_uses.keys()]


async def get_user_stats(user_id):
    result = await GameLog.select(GameLog.game, fn.GROUP_CONCAT(GameLog.result).alias('results'))\
        .where(GameLog.user_id == user_id)\
        .group_by(GameLog.game).dicts()
    return {i["game"]: str(i["results"]) for i in result}


async def get_user_casino_point(user_id):
    result = await GameLog.select(fn.SUM(GameLog.result).alias('points'))\
        .where(GameLog.user_id == user_id)\
        .dicts()
    return result[0]["points"] or 0


if __name__ == "__main__":
    import asyncio

    async def test():
        # x = await get_user_promos(357108179)
        # x = await add_new_promo_to_user(357108179, ' 152')
        x = await get_user_casino_point(357108179)
        print(x)


    asyncio.run(test())
