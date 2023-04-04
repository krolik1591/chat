from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import GAME_ERR1


def game_menu_err(err):
    text = ''
    if err == 1:
        text = GAME_ERR1.format()   # user doesnt choice bet

    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)