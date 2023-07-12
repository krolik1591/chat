import time

from peewee import fn

from bot.db.models import GameLog, PromoCodes, Transactions, UsersPromoCodes

TWO_WEEK = 1209600  # default time active promo-code


async def add_new_promo_code(name, _type, bonus, number_of_users=float('Infinity'), number_of_uses=1):
    return await PromoCodes.create(name=name, bonus=bonus, type=_type,
                                   date_start=time.time(), date_end=time.time() + TWO_WEEK,
                                   number_of_uses=number_of_uses, number_of_users=number_of_users)


async def user_activated_promo_code(user_id, promo_name):
    promo_info = await get_promo_code_info(promo_name)
    return await UsersPromoCodes.create(user_id=user_id, promo_name=promo_name, promo_type=promo_info.type,
                                        date_activated=time.time())


async def get_promo_code_info(name):
    return await PromoCodes.select(PromoCodes).where(PromoCodes.name == name).first()


async def get_all_active_promo_code():
    now = time.time()
    return await PromoCodes.select(PromoCodes.name).where(PromoCodes.date_start < now < PromoCodes.date_end).scalars()


#
# async def need_a_bonus(user_id):
#     now = time.time()
#     active_promo_code = await UsersPromoCodes.select(UsersPromoCodes.date_of_using, UsersPromoCodes.date_end,
#                                                      UsersPromoCodes.promo_name) \
#         .where(UsersPromoCodes.user_id == user_id, UsersPromoCodes.date_of_using < now < UsersPromoCodes.date_end,
#                ).dicts().first()
#     if not active_promo_code:
#         return
#
#     all_tx = await Transactions.select() \
#         .where(active_promo_code['date_of_using'] < Transactions.utime < active_promo_code['date_end'],
#                Transactions.user_id == user_id).count()
#
#     return all_tx


async def get_active_promo_code(user_id, promo_type):
    now = time.time()

    user_promo_codes = await UsersPromoCodes.select().where(UsersPromoCodes.user_id == user_id,
                                                            UsersPromoCodes.promo_type == promo_type).order_by(
        UsersPromoCodes.date_activated.desc()).dicts()

    if not user_promo_codes:
        return None

    active_promo = None
    for promo_code in user_promo_codes[:3]:
        promo_info = await get_promo_code_info(promo_code["promo_name"])
        if promo_info.date_start < now < promo_info.date_end:
            active_promo = promo_info
            break

    return active_promo


async def need_a_bonus(user_id):
    active_promo = await get_active_promo_code(user_id, 'balance')
    if not active_promo:
        return False

    tx_count = await Transactions.select().where(active_promo.date_start < Transactions.utime < active_promo.date_end,
                                                 Transactions.user_id == user_id).count()
    if active_promo.number_of_uses - tx_count > 0:
        return active_promo
    else:
        return False


async def update_wagers(user_id, bonus, promo_code):
    return await UsersPromoCodes.update({UsersPromoCodes.min_wager: bonus, UsersPromoCodes.wager: bonus * 10}).where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_code.name
    )


async def get_info_from_user_promo_codes(user_id, promo_name):
    return await UsersPromoCodes.select().where(
        UsersPromoCodes.user_id == user_id, UsersPromoCodes.promo_name == promo_name).order_by(
        UsersPromoCodes.date_activated.desc()
    ).first()


async def get_sum_bets_from_activated_promo_and_min_wager(user_id):
    promo_code = await get_active_promo_code(user_id, 'balance')
    user_promo_info = await get_info_from_user_promo_codes(user_id, promo_code.name)
    result = await GameLog.select(fn.SUM(GameLog.bet)).where(
        GameLog.user_id == user_id, user_promo_info.date_activated < GameLog.timestamp < promo_code.date_end,
        GameLog.balance_type == 'general').scalar()
    return result, user_promo_info.min_wager


if __name__ == "__main__":
    import asyncio
    from bot.db import db


    async def test():
        # await add_new_promo_code('pipiska', 'balance', 100)
        # await user_activated_promo_code(357108179, 'pipiska')
        # x = await get_date_activated_promo_by_user(357108179, 'pipiska')
        # x = await get_promo_code_info('huuuuuuiii')
        # x = await need_a_bonus(357108179)
        x = await get_sum_bets_from_activated_promo_and_min_wager(357108179)
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
