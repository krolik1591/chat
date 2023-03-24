from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_MENU_TEXT2


def withdraw_menu_address():
    text = WITHDRAW_MENU_TEXT2.format()
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Назад', callback_data="withdraw")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)