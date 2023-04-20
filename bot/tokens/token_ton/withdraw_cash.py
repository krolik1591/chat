import time

from bot.db import db, methods
from bot.menus.wallet_menus import withdraw_menu_err, withdraw_menu
from bot.tokens.token_ton import TonWrapper, find_withdraw_tx


async def withdraw_cash_to_user(state, user_withdraw_address, withdraw_amount_ton, user_id, token, manual_tx):
    master_wallet = TonWrapper.INSTANCE.master_wallet
    withdraw_amount_price = withdraw_amount_ton * token.price

    master_balance_nano = await master_wallet.get_balance()
    master_balance_ton = master_balance_nano / 1e9

    if withdraw_amount_ton >= master_balance_ton:
        await db.update_user_balance(user_id, token.token_id, withdraw_amount_price)  # return tokens to user

        text, keyboard = withdraw_menu_err.insufficient_funds_master()
        await state.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        return

    if manual_tx is False:
        await db.add_new_manual_tx(user_id, withdraw_amount_ton * 1e9, token.token_id, token.price,
                                   user_withdraw_address, time.time(), is_manual=False)

    await master_wallet.transfer_ton(user_withdraw_address, withdraw_amount_ton)

    # FIXME VERY WRONG!! SO SHIT!!!!! CRINGEEEEEE!!!!!

    is_found = await find_withdraw_tx(user_withdraw_address, withdraw_amount_ton, user_id, master_wallet.address)

    if not is_found:
        await db.update_user_balance(user_id, token.token_id, withdraw_amount_price)

    text, keyboard = withdraw_menu.withdraw_result(is_found)  # transfer money withdraw_queued
    await state.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)

