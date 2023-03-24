from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT


def deposit_menu(balances: dict, token_price):
    balances_text = '\n'.join([balance_text(i) for i in balances.values()])
    text = DEPOSIT_MENU_TEXT.format(balances=balances_text, token_price=token_price)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='📥 Поповнити', callback_data="replenish"),
            InlineKeyboardButton(text='📤 Вивести', callback_data="withdraw")
        ],
        [
            InlineKeyboardButton(text='💳 Як придбати TON?', callback_data="how_to_buy")
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)