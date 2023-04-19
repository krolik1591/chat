from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import MIN_WITHDRAW
from bot.texts import WITHDRAW_MENU_TEXT1


def withdraw_menu_amount(token_price):
    ton_amount = MIN_WITHDRAW / token_price
    text = WITHDRAW_MENU_TEXT1.format(min_withdraw=MIN_WITHDRAW, ton_amount=ton_amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Мій гаманець', callback_data="deposit")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)