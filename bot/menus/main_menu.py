from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import MENU_TEXT


def main_menu(balances: dict):
    balances_text = '\n'.join([balance_text(i) for i in balances.values()])

    text = MENU_TEXT.format(balances=balances_text)
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
