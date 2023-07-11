import time

from bot.db.models import PromoCodes, UsersPromoCodes


async def add_new_promo_code(name, type, bonus, wager, number_of_users=float('Infinity'), number_of_uses=1, date_end=None):
    return await PromoCodes.create(name=name, bonus=bonus, wager=wager, date_end=date_end, number_of_uses=number_of_uses,
                                   number_of_users=number_of_users, type=type)


async def get_promo_code_info(name):
    result = await PromoCodes.select(PromoCodes).where(PromoCodes.name == name)
    return result[0]


async def user_activated_promo(user_id, name, date_end=None):
    return await UsersPromoCodes.create(user_id=user_id, promo_name=name, date_of_using=time.time(), date_end=date_end)


if __name__ == "__main__":
    import asyncio

    async def test():
        # await add_new_promo_code('hui', 'balance', 20, 200)
        # x = await get_promo_code_info('hui')
        # print(x.number_of_users > 9999)
        await user_activated_promo(357108179, 'hui')


    asyncio.run(test())
