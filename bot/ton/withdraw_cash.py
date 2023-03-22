from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import get_token_by_id
from bot.handlers.deposit_heandlers.d01_replenish import prepare_wallets_to_work


async def withdraw_cash_to_user(master_wallet, user_withdraw_address, amount):
    print('mw', master_wallet.address, await master_wallet.get_balance())

    x = await master_wallet.transfer_ton(user_withdraw_address, amount)     #
    print(x)
