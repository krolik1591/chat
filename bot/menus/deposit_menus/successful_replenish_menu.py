from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import SUCCESSFUL_REPLENISH_MENU


def successful_replenish_menu(amount):
    text = SUCCESSFUL_REPLENISH_MENU.format(amount=amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [

        [
            InlineKeyboardButton(text='ОК', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)