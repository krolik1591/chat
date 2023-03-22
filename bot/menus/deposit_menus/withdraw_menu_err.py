from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_ERR1, WITHDRAW_ERR2, \
    WITHDRAW_ERR3, WITHDRAW_ERR4, WITHDRAW_ERR5


def withdraw_menu_err(err):
    if err == 1:
        text = WITHDRAW_ERR1.format()   # round_user_withdraw < MIN_WITHDRAW
    elif err == 2:
        text = WITHDRAW_ERR2.format()   # user balance < MIN_WITHDRAW
    elif err == 3:
        text = WITHDRAW_ERR3.format()   # test.net address
    elif err == 4:
        text = WITHDRAW_ERR4.format()   # incorrect address
    elif err == 5:
        text = WITHDRAW_ERR5.format()   # round_user_withdraw > user_balance


    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)