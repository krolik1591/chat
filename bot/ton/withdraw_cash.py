from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import get_token_by_id, update_user_balance
from bot.handlers.deposit_heandlers.d01_replenish import prepare_wallets_to_work
from bot.menus.deposit_menus.withdraw_menu_err import withdraw_menu_err


async def withdraw_cash_to_user(master_wallet, user_withdraw_address, withdraw_amount_ton, user_id, token, state):
    master_balance_nano = await master_wallet.get_balance()
    master_balance_ton = master_balance_nano / 1e9
    print(master_balance_ton, withdraw_amount_ton)

    if master_balance_ton > withdraw_amount_ton:
        transfer_result = await master_wallet.transfer_ton(user_withdraw_address, withdraw_amount_ton)
        print('transfer_result:', transfer_result)

        withdraw_amount_price = -(withdraw_amount_ton * token.price)
        await update_user_balance(user_id, token.token_id, withdraw_amount_price)
    else:
        last_msg = (await state.get_data()).get('last_msg_id')

        text, keyboard = withdraw_menu_err(6)
        await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=user_id, message_id=last_msg)