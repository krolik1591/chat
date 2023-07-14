import time

from peewee import fn

from bot.db.models import GameLog, PromoCodes, Transactions, UsersPromoCodes

# 1209600 == 2 week
ACTIVE_PROMO_CODE = 1209600  # default time of activity of the promo code


async def add_new_promo_code(name, _type, bonus, duration, min_wager=1, wager=10, existence_promo=ACTIVE_PROMO_CODE,
                             number_of_users=float('Infinity'), number_of_uses=1, special_users=None):
    return await PromoCodes.create(name=name, bonus=bonus, type=_type, special_users=special_users,
                                   date_start=time.time(), date_end=time.time() + existence_promo,
                                   number_of_uses=number_of_uses, number_of_users=number_of_users,
                                   duration=duration, min_wager=min_wager, wager=wager)


async def user_activated_promo_code(user_id, promo_name):
    promo_info = await get_promo_code_info(promo_name)
    return await UsersPromoCodes.create(
        user_id=user_id, promo_name=promo_name, promo_type=promo_info.type,
        date_activated=time.time(), date_end=time.time() + promo_info.duration, is_active=True)


async def get_promo_code_info(name):
    return await PromoCodes.select(PromoCodes).where(PromoCodes.name == name).first()


async def get_users_whose_promo_code_expire(time_to_end):
    print(time_to_end, time_to_end - 3600)
    return await UsersPromoCodes.select(UsersPromoCodes.user_id).where(
        time_to_end > UsersPromoCodes.date_end > time_to_end - 3600, UsersPromoCodes.won == 0,
        UsersPromoCodes.is_active == 1).scalars()


async def get_all_available_promo_code_for_user(user_id):
    now = time.time()
    result = []

    promo_codes = await PromoCodes.select(PromoCodes).where(
        now < PromoCodes.date_end)

    for code in promo_codes:
        if code.special_users is None:
            result.append(code.name)
        else:
            special_users = code.special_users.split(',')
            if str(user_id) in special_users:
                result.append(code.name)

    return result


async def get_active_promo_code_from_promo_codes(user_id, promo_type):
    user_promo_code = await get_active_promo_code_from_user_promo_codes(user_id, promo_type)

    if not user_promo_code:
        return None

    promo_code_info = await get_promo_code_info(user_promo_code.promo_name)
    return promo_code_info


async def get_active_promo_code_from_user_promo_codes(user_id, promo_type):
    now = time.time()
    return await UsersPromoCodes.select(UsersPromoCodes).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_type == promo_type, UsersPromoCodes.is_active == 1,
        now < UsersPromoCodes.date_end).order_by(UsersPromoCodes.userspromocodes_id.desc()
                                                 ).first()


async def need_a_bonus(user_id):
    active_promo = await get_active_promo_code_from_promo_codes(user_id, 'balance')
    if not active_promo:
        return False

    tx_count = await Transactions.select().where(active_promo.date_start < Transactions.utime < active_promo.date_end,
                                                 Transactions.user_id == user_id).count()
    if active_promo.number_of_uses - tx_count > 0:
        return active_promo
    else:
        return False


async def update_wagers_and_bonus(user_id, bonus, promo_code):
    return await UsersPromoCodes.update({
        UsersPromoCodes.min_wager: int(promo_code.min_wager) * bonus,
        UsersPromoCodes.wager: int(promo_code.wager) * bonus,
        UsersPromoCodes.bonus: bonus}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_code.name
    )


async def get_info_from_user_promo_codes(user_id, promo_name):
    return await UsersPromoCodes.select().where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_name).order_by(
        UsersPromoCodes.date_activated.desc()
    ).first()


async def get_sum_bets_and_promo_info(user_id):
    promo_code = await get_active_promo_code_from_promo_codes(user_id, 'balance')
    user_promo_info = await get_info_from_user_promo_codes(user_id, promo_code.name)
    result = await GameLog.select(fn.SUM(GameLog.bet)).where(
        GameLog.user_id == user_id, user_promo_info.date_activated < GameLog.timestamp < promo_code.date_end,
        GameLog.balance_type == 'general').scalar()
    return result, user_promo_info


async def min_wager_condition_accepted(user_id, promo_name):
    return await UsersPromoCodes.update({UsersPromoCodes.won: True}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_name
    )


async def deactivate_user_promo_code(user_id, promo_name):
    now = time.time()
    return await UsersPromoCodes.update({UsersPromoCodes.is_active: 0}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_name, now < UsersPromoCodes.date_end,
        UsersPromoCodes.is_active == 1)


if __name__ == "__main__":
    import asyncio
    from bot.db import db


    async def test():
        # await add_new_promo_code('putin huilo3', 'balance', 100, 3600 * 6)
        # await user_activated_promo_code(357108179, 'putin huilo', 0)
        # x = await get_active_promo_code_from_promo_codes(357108179, 'putin huilo')
        x = await user_activated_promo_code(357108179, 'putin loh')
        # x = await get_all_available_promo_code_for_user(357108179)
        y = await get_users_whose_promo_code_expire(int(time.time()) + 3600 * 5)
        # x = await get_active_promo_code_from_user_promo_codes(357108179, 'balance')
        print(x.date_end < int(time.time()) + 3600 * 5)
        print(y)
        # await db.add_new_transaction(
        #     user_id=357108179,
        #     token_id="ton",
        #     amount=500,
        #     tx_type=3,  # withdraw
        #     tx_address='qgr4hgr',
        #     tx_hash='gwrgher5gh',
        #     logical_time=6516541641,
        #     utime=time.time(),
        #     comment='pohui'),
        pass


    asyncio.run(test())
