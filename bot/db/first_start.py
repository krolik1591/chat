from .db import database, Token, User, Balances, Transactions, GameLogs, objects


async def first_start():
    with objects.allow_sync():

        if Token.table_exists():
            return

        print("First start, creating tables...")

        database.create_tables([Token, User, Balances, Transactions, GameLogs])

        Token(token='demo', price=1, icon='🔥').save()
        Token(token='ton', price=10, icon='🔥').save()
