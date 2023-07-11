import time

from bot.db.models import PromoCodes, Transactions, UsersPromoCodes


async def add_new_promo_code(name, type, bonus, wager, number_of_users=float('Infinity'), number_of_uses=1,
                             date_end=None):
    return await PromoCodes.create(name=name, bonus=bonus, wager=wager, date_end=date_end,
                                   number_of_uses=number_of_uses,
                                   number_of_users=number_of_users, type=type)


async def user_activated_promo_code(user_id, name, date_end=None):
    return await UsersPromoCodes.create(user_id=user_id, promo_name=name, date_of_using=time.time(), date_end=date_end)


async def get_promo_code_info(name):
    result = await PromoCodes.select(PromoCodes).where(PromoCodes.name == name)
    return result[0]


async def get_all_active_promo_code():
    result = await PromoCodes.select(PromoCodes.name).where(PromoCodes.status == 1).scalars()
    return result


async def need_a_bonus(user_id):
    now = time.time()
    active_promo_code = await UsersPromoCodes.select(UsersPromoCodes.date_of_using, UsersPromoCodes.date_end,
                                                     UsersPromoCodes.promo_name) \
        .where(UsersPromoCodes.user_id == user_id, UsersPromoCodes.date_of_using < now < UsersPromoCodes.date_end,
               ).dicts().first()
    if not active_promo_code:
        return

    all_tx = await Transactions.select() \
        .where(active_promo_code['date_of_using'] < Transactions.utime < active_promo_code['date_end'],
               Transactions.user_id == user_id).count()

    return all_tx


if __name__ == "__main__":
    import asyncio
    from bot.db import db


    async def test():
        # await add_new_promo_code('huuuuuuiii', 'balance', 20, 200)
        # x = await get_promo_code_info('huuuuuuiii')
        # print(x)
        # await user_activated_promo_code(357108179, 'huuuuuuiii')
        x = await need_a_bonus(357108179)
        # print(x)

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
