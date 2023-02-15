from bot.db import first_start
from bot.db.db import Balances


async def get_user_balances(user_id):
    # token_name, token_icon, amount
    return await Balances.get(user_id=user_id)


if __name__ == "__main__":

    async def test():
        await first_start()
        print(await get_user_balances(1))

    import asyncio
    asyncio.run(test())

