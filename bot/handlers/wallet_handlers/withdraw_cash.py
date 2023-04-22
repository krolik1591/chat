from bot.db import db
from bot.menus.wallet_menus import withdraw_menu_err, withdraw_menu
from bot.tokens import Token, InsufficientFunds
from bot.tokens.token_ton import find_withdraw_tx


async def withdraw_cash_to_user(bot, withdraw_address, withdraw_amount, user_id, token: Token):

    try:
        await token.can_transfer(withdraw_amount)
    except InsufficientFunds:
        await db.update_user_balance(user_id, token.token_id, withdraw_amount)  # return tokens to user

        text, keyboard = withdraw_menu_err.insufficient_funds_master()
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        return

    withdraw_amount_ton = await token.transfer(withdraw_address, withdraw_amount)

    # FIXME VERY WRONG!! SO SHIT!!!!! CRINGEEEEEE!!!!!

    is_found = await find_withdraw_tx(withdraw_address, withdraw_amount_ton, user_id)

    if not is_found:
        # return tokens to user
        await db.update_user_balance(user_id, token.token_id, withdraw_amount)

    text, keyboard = withdraw_menu.withdraw_result(is_found)  # transfer money withdraw_queued
    await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)

