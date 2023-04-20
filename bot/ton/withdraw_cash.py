import time

from bot.db.methods import add_new_manual_tx, update_user_balance
from bot.menus.deposit_menus import withdraw_menu_err, withdraw_menu
from bot.ton.process_withdraw_tx import process_withdraw_tx


async def withdraw_cash_to_user(state, user_withdraw_address, withdraw_amount_ton, user_id, token, manual_tx):
    master_wallet = state.bot.ton_client.master_wallet
    withdraw_amount_price = withdraw_amount_ton * token.price

    master_balance_nano = await master_wallet.get_balance()
    master_balance_ton = master_balance_nano / 1e9

    if master_balance_ton > withdraw_amount_ton:

        if manual_tx is False:
            await add_new_manual_tx(user_id, withdraw_amount_ton * 10 ** 9, token.token_id, token.price,
                                    user_withdraw_address, time.time(), is_manual=False)

        await master_wallet.transfer_ton(user_withdraw_address, withdraw_amount_ton)

        withdraw_condition = await process_withdraw_tx(state, user_withdraw_address, withdraw_amount_ton, user_id,
                                                       master_wallet.address)

        await withdraw_approve(withdraw_condition, state, user_id, token, withdraw_amount_price)

    else:
        await update_user_balance(user_id, token.token_id, withdraw_amount_price)

        text_err, keyboard = withdraw_menu_err.withdraw_err_insufficient_funds_master()
        await state.bot.send_message(user_id, text_err, reply_markup=keyboard)


async def withdraw_approve(withdraw_condition, state, user_id, token, withdraw_amount_price):
    if withdraw_condition:
        text, keyboard = withdraw_menu.withdraw_result(withdraw_condition)  # transfer money withdraw_queued
        await state.bot.send_message(text=text, reply_markup=keyboard, chat_id=user_id)
    else:
        await update_user_balance(user_id, token.token_id, withdraw_amount_price)
        text, keyboard = withdraw_menu.withdraw_result(withdraw_condition)
        await state.bot.send_message(text=text, reply_markup=keyboard, chat_id=user_id)
