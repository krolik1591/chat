from .models import WithdrawTx, User, Transactions, GameLog, Wallets_key, manager, WoFTickets, Settings, WoFSettings, \
    PromoCodes, UsersPromoCodes


async def first_start():
    if User.table_exists():
        return

    print("First start, creating tables...")

    await manager.create_tables(Wallets_key, User, Transactions, WithdrawTx, GameLog, WoFTickets, Settings, WoFSettings,
                                PromoCodes, UsersPromoCodes)
