from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_MENU_TEXT1


def withdraw_menu_amount():
    text = WITHDRAW_MENU_TEXT1.format()
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Мій гаманець', callback_data="deposit")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)