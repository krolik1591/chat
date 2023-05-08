import time

from bot.db import db
from bot.menus.wallet_menus import withdraw_menu_err
from bot.tokens import InsufficientFunds, Token


async def withdraw_cash_to_user(bot, withdraw_address, withdraw_amount, user_id, token: Token, tx):

    try:
        await token.can_transfer(withdraw_amount)   #todo враховувати fee
    except InsufficientFunds:
        await db.update_user_balance(user_id, 'general', withdraw_amount)  # return tokens to user

        text, keyboard = withdraw_menu_err.insufficient_funds_master()
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        return

    transfer_text = f'withdrawv1{tx.withdrawtx_id}|{tx.utime}'

    await token.transfer(withdraw_address, withdraw_amount, transfer_text)
