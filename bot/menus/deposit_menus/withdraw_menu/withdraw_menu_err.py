from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_ERR1, WITHDRAW_ERR2, \
    WITHDRAW_ERR3, WITHDRAW_ERR4, WITHDRAW_ERR5, WITHDRAW_ERR6

WITHDRAW_ERR = {
    1: WITHDRAW_ERR1,   # round_user_withdraw < MIN_WITHDRAW
    2: WITHDRAW_ERR2,   # user balance < MIN_WITHDRAW
    3: WITHDRAW_ERR3,   # test.net address
    4: WITHDRAW_ERR4,   # incorrect address
    5: WITHDRAW_ERR5,   # round_user_withdraw > user_balance
    6: WITHDRAW_ERR6,   # end money on master wallet
}


def withdraw_menu_err(err):
    text = WITHDRAW_ERR[err]
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)