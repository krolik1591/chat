import time

from bot.db import db
from bot.menus.wallet_menus import withdraw_menu_err, withdraw_menu
from bot.tokens.token_ton import TonWrapper, find_withdraw_tx


async def withdraw_cash_to_user(bot, withdraw_address, withdraw_amount_ton, user_id, token, manual_tx):
    withdraw_amount = withdraw_amount_ton * token.price
    withdraw_amount_nanoton = withdraw_amount_ton * 1e9

    master_wallet = TonWrapper.INSTANCE.master_wallet

    master_balance_nanoton = await master_wallet.get_balance()

    if withdraw_amount_nanoton >= master_balance_nanoton:
        await db.update_user_balance(user_id, token.token_id, withdraw_amount)  # return tokens to user

        text, keyboard = withdraw_menu_err.insufficient_funds_master()
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        return

    if manual_tx is False:
        await db.add_new_manual_tx(user_id, withdraw_amount_nanoton, token.token_id, token.price,
                                   withdraw_address, time.time(), is_manual=False)

    await master_wallet.transfer_ton(withdraw_address, withdraw_amount_ton)

    # FIXME VERY WRONG!! SO SHIT!!!!! CRINGEEEEEE!!!!!

    is_found = await find_withdraw_tx(withdraw_address, withdraw_amount_ton, user_id, master_wallet.address)

    if not is_found:
        await db.update_user_balance(user_id, token.token_id, withdraw_amount)

    text, keyboard = withdraw_menu.withdraw_result(is_found)  # transfer money withdraw_queued
    await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)

