from .db import Token, User, Balances, Transactions, GameLogs, manager


async def first_start():
    if Token.table_exists():
        return

    print("First start, creating tables...")

    # await Token.create_table()
    await manager.create_tables(Token, User, Balances, Transactions, GameLogs)

    await Token.create(token_id='demo', price=1, icon='🔥')
    await Token.create(token_id='ton', price=10, icon='🔥')

