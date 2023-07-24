import time

from peewee import fn

from bot.db.models import User, Wallets_key


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


# admin

async def get_users_by_lang(lang):
    users = await User.select(User.user_id).where(User.lang == lang, User.is_blocked == 0)
    result = [user.user_id for user in users]
    return result


async def user_blocked_bot(tg_id, is_blocked=True):
    return await User.update({User.is_blocked: is_blocked}).where(User.user_id == tg_id)


async def is_user_blocked_bot(user_id):
    result = await User.select(User).where(User.user_id == user_id).first()
    return result.is_blocked


# balances


async def get_user_balances(user_id):
    result = await User.select(User.balance_demo, User.balance_promo, User.balance_general) \
        .where(User.user_id == user_id)
    if not result:
        raise ValueError
    return {
        'demo': result[0].balance_demo,
        'promo': result[0].balance_promo,
        'general': result[0].balance_general
    }


async def get_user_balance(user_id, balance_type):
    return (await get_user_balances(user_id))[balance_type]


async def update_user_balance(user_id, balance_type, balance_to_add):
    field = {
        'demo': User.balance_demo,
        'promo': User.balance_promo,
        'general': User.balance_general
    }[balance_type]

    return await User.update({field: fn.ROUND(field + balance_to_add, 5)}).where(User.user_id == user_id)


# wallets


async def create_user_wallet(tg_id, address, mnemonic):
    return await Wallets_key.create(user_id=tg_id, mnemonic=mnemonic, address=address)


async def get_all_user_wallets():
    return await Wallets_key.select(Wallets_key.user_id, Wallets_key.address, Wallets_key.mnemonic)


async def get_user_wallet(tg_id):
    return await Wallets_key.select().where(Wallets_key.user_id == tg_id).first()
