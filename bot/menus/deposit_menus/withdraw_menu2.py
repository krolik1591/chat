from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT, REPLENISH_MENU_TEXT, WITHDRAW_MENU_TEXT1, WITHDRAW_MENU_TEXT2


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