from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import MENU_TEXT


def main_menu(main_balance, demo_balance):
    text = MENU_TEXT.format(main_balance=main_balance, demo_balance=demo_balance)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Ігри', callback_data="all_games"),
        ],
        [
            InlineKeyboardButton(text='Депозит', callback_data="deposit")
        ],
        [
            InlineKeyboardButton(text='Налаштування', callback_data="settings")
        ],
        [
            InlineKeyboardButton(text='Підтримка', callback_data="support"),
            InlineKeyboardButton(text='Реклама', callback_data="spam")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
