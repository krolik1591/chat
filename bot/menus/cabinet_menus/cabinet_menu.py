from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts.texts import CABINET_MENU_TEXT


def cabinet_menu():
    text = CABINET_MENU_TEXT
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='💎 Депозит', callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text='👬 Реферали', callback_data="referrals_menu")
        ],
        [
            InlineKeyboardButton(text='‹ Назад', callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
