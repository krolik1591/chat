from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT, SUCCESSFUL_REPLENISH_MENU


def successful_replenish_menu(amount):
    text = SUCCESSFUL_REPLENISH_MENU.format(amount=amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [

        [
            InlineKeyboardButton(text='ОК', callback_data="wtfOK")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)