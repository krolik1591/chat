from .db import Token, User, Balance, Transaction, GameLog, Wallets_key, manager


async def first_start():
    if Token.table_exists():
        return

    print("First start, creating tables...")

    # await Token.create_table()
    await manager.create_tables(Wallets_key, Token, User, Balance, Transaction, GameLog)

    await Token.create(name='DEMO', price=1, icon='🦶')
    await Token.create(name='TON', price=100, icon='💎')