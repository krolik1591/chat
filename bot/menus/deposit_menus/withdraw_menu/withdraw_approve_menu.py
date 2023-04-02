from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_APPROVE


def withdraw_approve_menu(user_withdraw_amount):
    user_withdraw_amount_ton = user_withdraw_amount/100
    text = WITHDRAW_APPROVE.format(user_withdraw_amount=user_withdraw_amount, user_withdraw_amount_ton=user_withdraw_amount_ton)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='В меню', callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)