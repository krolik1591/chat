from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT, REPLENISH_MENU_TEXT, WITHDRAW_MENU_TEXT1


def withdraw_menu():
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