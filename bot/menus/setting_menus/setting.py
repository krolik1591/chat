from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts.texts import SETTING_TEXT


def setting_menu():
    text = SETTING_TEXT
    kb = _keyboard()
    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Змінити мову', callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text='‹ Назад', callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
