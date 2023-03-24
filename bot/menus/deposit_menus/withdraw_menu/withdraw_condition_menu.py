from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import PAYMENT_CONFIRMED, PAYMENT_DENIED


def withdraw_condition_menu(condition):
    if condition:
        text = PAYMENT_CONFIRMED.format()   # round_user_withdraw < MIN_WITHDRAW
    else:
        text = PAYMENT_DENIED.format()   # user balance < MIN_WITHDRAW




    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)