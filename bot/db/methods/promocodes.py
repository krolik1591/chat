import time

from peewee import fn

from bot.db.models import GameLog, PromoCodes, Transactions, UsersPromoCodes

# 1209600 == 2 week
ACTIVE_PROMO_CODE = 1209600  # default time of activity of the promo code


async def add_new_promo_code(name, _type, bonus, duration, min_wager=1, wager=10, existence_promo=ACTIVE_PROMO_CODE,
                             number_of_users=float('Infinity'), max_deposits=1, special_users=None):
    if _type == 'ticket':
        min_wager = 0

    return await PromoCodes.create(name=name, bonus=bonus, type=_type, special_users=special_users,
                                   date_start=time.time(), date_end=time.time() + existence_promo,
                                   max_deposits=max_deposits, number_of_users=number_of_users,
                                   duration=duration, min_wager=min_wager, wager=wager)


async def user_activated_promo_code(user_id, promo_name):
    promo_info = await get_promo_code_info(promo_name)
    return await UsersPromoCodes.create(
        user_id=user_id, promo_name=promo_name, promo_type=promo_info.type,
        date_activated=time.time(), date_end=time.time() + promo_info.duration, is_active=True)


async def get_promo_code_info(name):
    return await PromoCodes.select(PromoCodes).where(PromoCodes.name == name).first()


async def get_users_whose_promo_code_expire(time_gt, time_lt):
    result = await UsersPromoCodes.select(UsersPromoCodes.user_id).join(PromoCodes).where(
        time_lt < UsersPromoCodes.date_end,
        UsersPromoCodes.date_end < time_gt,
        UsersPromoCodes.won == 0,
        UsersPromoCodes.is_active == 1,
        PromoCodes.type == 'balance'    # wof promo ticket doesn't have end date
    ).scalars()

    return result


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


async def get_all_active_user_promo_codes(user_id):
    now = time.time()

    return await UsersPromoCodes.select(UsersPromoCodes).where(
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.is_active == 1,
        now < UsersPromoCodes.date_end)


async def need_a_bonus(user_id):
    active_promo = await get_all_info_user_promo_code(user_id, 'balance')
    if not active_promo:
        return 0

    tx_count = await Transactions.select().where(
        active_promo.date_activated < Transactions.utime, Transactions.utime < active_promo.date_end,
        Transactions.user_id == user_id).count()

    if active_promo.promocode.max_deposits - tx_count > 0:
        return active_promo
    else:
        return 0


async def update_wagers_and_bonus(user_id, bonus, promo_code):
    return await UsersPromoCodes.update({
        UsersPromoCodes.min_wager: float(promo_code.min_wager) * bonus,
        UsersPromoCodes.wager: float(promo_code.wager) * bonus,
        UsersPromoCodes.bonus: bonus}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_code.name
    )


async def get_all_info_user_promo_code(user_id, promo_type):
    return await UsersPromoCodes.select(PromoCodes, UsersPromoCodes).where(
        UsersPromoCodes.user_id == user_id,
        PromoCodes.type == promo_type,
        UsersPromoCodes.is_active == 1
    ).join(PromoCodes, attr='promocode').first()


async def get_sum_bets_and_promo_info(user_id):
    balance_promo_code = await get_all_info_user_promo_code(user_id, 'balance')
    ticket_promo_code = await get_all_info_user_promo_code(user_id, 'ticket')

    first_activated = min(getattr(balance_promo_code, 'date_activated', float('Infinity')),
                          getattr(ticket_promo_code, 'date_activated', float('Infinity')))

    bets_sum = await GameLog.select(fn.SUM(GameLog.bet)).where(
        GameLog.user_id == user_id, first_activated < GameLog.timestamp,
        GameLog.balance_type == 'general').scalar() or 0

    return bets_sum, balance_promo_code, ticket_promo_code


async def min_wager_condition_accepted(user_id, promo_name):
    return await UsersPromoCodes.update({UsersPromoCodes.won: True}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_name
    )


async def deactivate_user_promo_code(user_id):
    now = time.time()
    return await UsersPromoCodes.update({UsersPromoCodes.is_active: 0}).where(
        UsersPromoCodes.user_id == user_id, now < UsersPromoCodes.date_end, UsersPromoCodes.is_active == 1)


if __name__ == "__main__":
    import asyncio
    from bot.db import db


    async def test():
        # await add_new_promo_code('putin loh', 'ticket', 100, 3600 * 6)
        # x = await get_active_promo_code_from_promo_codes(357108179, 'putin huilo')
        # x = await user_activated_promo_code(357108179, 'putin loh')
        # x = await get_all_available_promo_code_for_user(357108179)
        # x = await need_a_bonus(357108179)
        # x = await db.need_a_bonus(357108179)
        # y = await get_all_info_user_promo_code(357108179, 'balance')
        # x, balance, ticket = await get_sum_bets_and_promo_info(357108179)
        # print(balance.promo_name_id)
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
