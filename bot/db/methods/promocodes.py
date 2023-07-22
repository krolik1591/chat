import time

from peewee import fn

from bot.db.methods import get_active_wheel_info
from bot.db.models import GameLog, PromoCodes, Transactions, UsersPromoCodes, WoFTickets

# 1209600 == 2 week
from bot.utils.rounding import round_down

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
    if promo_info.type == 'ticket':
        bonus_tickets = promo_info.bonus
    else:
        bonus_tickets = None
    return await UsersPromoCodes.create(
        user_id=user_id, promo_name=promo_name, is_active=True, available_bonus_tickets=bonus_tickets,
        date_activated=time.time(), date_end=time.time() + promo_info.duration)


async def get_promo_code_info(name):
    return await PromoCodes.select(PromoCodes).where(PromoCodes.name == name).first()


async def get_users_whose_promo_code_expire(time_gt, time_lt):
    result = await UsersPromoCodes.select(UsersPromoCodes.user_id).join(PromoCodes).where(
        time_lt < UsersPromoCodes.date_end,
        UsersPromoCodes.date_end < time_gt,
        UsersPromoCodes.won == 0,
        UsersPromoCodes.is_active == 1,
        PromoCodes.type == 'balance'  # wof promo ticket doesn't have end date
    ).scalars()

    return result


async def get_all_available_promo_code_for_user(user_id):
    now = time.time()
    result = []

    promo_codes = await PromoCodes.select(PromoCodes).where(
        now < PromoCodes.date_end)

    for code in promo_codes:
        all_exist_user_promos = await get_all_exist_user_promo_codes(user_id)
        if code.name in all_exist_user_promos:
            continue

        if code.number_of_users != float("Infinity"):
            times_of_used = await get_times_promo_used(code.name)
            if times_of_used >= code.number_of_users:
                continue

        if code.special_users is None:
            result.append(code.name)
        else:
            special_users = code.special_users.split(',')
            if str(user_id) in special_users:
                result.append(code.name)

    return result


async def get_all_exist_user_promo_codes(user_id):
    return await UsersPromoCodes.select(fn.DISTINCT(UsersPromoCodes.promo_name_id)).where(
        UsersPromoCodes.user_id == user_id).scalars()


async def get_times_promo_used(promo_name):
    now = time.time()
    return await UsersPromoCodes.select(PromoCodes, UsersPromoCodes).where(
        UsersPromoCodes.promo_name == promo_name,
        PromoCodes.date_start < now,
        PromoCodes.date_end > now
    ).join(PromoCodes).count()


async def get_all_active_user_promo_codes(user_id):
    now = time.time()

    return await UsersPromoCodes.select(UsersPromoCodes, PromoCodes).where(
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.is_active == 1,
        now < UsersPromoCodes.date_end).join(PromoCodes, attr=('promocode'))


async def need_a_bonus(user_id):
    active_promo = await get_all_info_user_promo_code_by_type(user_id, 'balance')
    if not active_promo:
        return 0

    tx_count = await Transactions.select().where(
        active_promo.date_activated < Transactions.utime, Transactions.utime < active_promo.date_end,
        Transactions.user_id == user_id, Transactions.tx_type == 1).count()

    if active_promo.promocode.max_deposits - tx_count > 0:
        return active_promo
    else:
        return 0


async def update_wagers_and_bonus(user_id, bonus, promo_code):
    return await UsersPromoCodes.update({
        UsersPromoCodes.deposited_min_wager: fn.ROUND(UsersPromoCodes.deposited_min_wager + float(
            promo_code.promocode.min_wager) * bonus, 2),
        UsersPromoCodes.deposited_wager: fn.ROUND(UsersPromoCodes.deposited_wager + float(promo_code.promocode.wager) * bonus, 2),
        UsersPromoCodes.deposited_bonus: fn.ROUND(UsersPromoCodes.deposited_bonus + bonus, 2)}).where(
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.promo_name == promo_code.promo_name_id
    )


async def get_all_info_user_promo_code_by_type(user_id, promo_type):
    return await UsersPromoCodes.select(PromoCodes, UsersPromoCodes).where(
        UsersPromoCodes.user_id == user_id,
        PromoCodes.type == promo_type,
        UsersPromoCodes.is_active == 1
    ).join(PromoCodes, attr='promocode').first()


async def can_deactivate_ticket_promo(user_id, promo_name):
    return await UsersPromoCodes.select().where(
        UsersPromoCodes.promo_name_id == promo_name,
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.available_bonus_tickets == 0,
        UsersPromoCodes.is_active == 1,
        UsersPromoCodes.won == 0)


async def get_sum_bets_and_promo_info(user_id):
    balance_promo_code = await get_all_info_user_promo_code_by_type(user_id, 'balance')
    ticket_promo_code = await get_all_info_user_promo_code_by_type(user_id, 'ticket')

    first_activated = min(getattr(balance_promo_code, 'date_activated', float('Infinity')),
                          getattr(ticket_promo_code, 'date_activated', float('Infinity')))

    bets_sum_min_wager = await GameLog.select(fn.SUM(GameLog.bet)).where(
        GameLog.user_id == user_id, first_activated < GameLog.timestamp,
        GameLog.balance_type == 'general').scalar() or 0

    bets_sum_promo = await GameLog.select(fn.SUM(GameLog.bet)).where(
        GameLog.user_id == user_id, first_activated < GameLog.timestamp,
        GameLog.balance_type == 'promo').scalar() or 0

    bets_sum_wager = bets_sum_min_wager + bets_sum_promo

    return balance_promo_code, ticket_promo_code, bets_sum_min_wager, bets_sum_wager


async def update_won_condition(user_id, promo_name):
    return await UsersPromoCodes.update({UsersPromoCodes.won: True}).where(
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.promo_name == promo_name
    )


async def deactivate_user_promo_code(user_id, promo_name):
    return await UsersPromoCodes.update({UsersPromoCodes.is_active: 0}).where(
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.promo_name_id == promo_name,
        UsersPromoCodes.is_active == 1)


async def get_available_tickets_count(user_id, promo_name):
    result = await UsersPromoCodes.select(UsersPromoCodes).where(
        UsersPromoCodes.promo_name_id == promo_name,
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.is_active == 1
    )
    return result[0].available_bonus_tickets


async def update_available_tickets_count(user_id, promo_name, count):
    return await UsersPromoCodes.update(
        {UsersPromoCodes.available_bonus_tickets: UsersPromoCodes.available_bonus_tickets + count}).where(
        UsersPromoCodes.promo_name_id == promo_name,
        UsersPromoCodes.user_id == user_id,
        UsersPromoCodes.is_active == 1
    )


async def get_unique_promocode_from_wof_tickets():
    return await WoFTickets.select(fn.DISTINCT(WoFTickets.promo_id)).scalars()


async def get_unique_users_by_promo_code(promo_name):
    return await WoFTickets.select(fn.DISTINCT(WoFTickets.user_id)).where(WoFTickets.promo_id == promo_name).scalars()


if __name__ == "__main__":
    import asyncio
    from bot.db import db


    async def test():
        # await add_new_promo_code('putin loh2', 'balance', 100, 3600 * 24)
        # x = await get_active_promo_code_from_promo_codes(357108179, 'putin huilo')
        # x = await user_activated_promo_code(357108179, 'putin loh2')
        # x = await get_all_available_promo_code_for_user(357108179)

        x = await get_all_exist_user_promo_codes(357108179)

        # x = await db.get_all_active_user_promo_codes(357108179)
        print(x)
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
