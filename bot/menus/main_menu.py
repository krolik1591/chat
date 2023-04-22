from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text
from bot.consts.texts import MENU_TEXT


def main_menu(balances: dict):
    text = MENU_TEXT.format(balances=balances_text(balances))
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='🎲 Ігри', callback_data="all_games"),
        ],
        [
            InlineKeyboardButton(text='💎 Депозит', callback_data="wallet_menu")
        ],
        [
            InlineKeyboardButton(text='⚙️ Налаштування', callback_data="settings")
        ],
        [
            InlineKeyboardButton(text='📢 Реклама', callback_data="spam"),
            InlineKeyboardButton(text='💬 Підтримка', callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
