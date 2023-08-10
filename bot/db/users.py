import time

from peewee import fn

from bot.db.models import User


# users


async def create_new_user(tg_id, username, referrer, start_points):
    return await User.create(user_id=tg_id, username=username, timestamp_registered=time.time(),
                             timestamp_last_active=time.time(), referrer=referrer, balance_demo=start_points)


async def update_username(tg_id, username):
    return await User.update({User.username: username}).where(User.user_id == tg_id)


async def get_user_lang(tg_id):
    user_lang = await User.select(User.lang).where(User.user_id == tg_id)
    if not user_lang:
        raise ValueError
    return user_lang[0].lang


async def set_user_lang(tg_id, new_lang):
    return await User.update({User.lang: new_lang}).where(User.user_id == tg_id)


async def set_user_last_active(tg_id):
    return await User.update({User.timestamp_last_active: time.time()}).where(User.user_id == tg_id)
