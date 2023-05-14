from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text, get_balance_icon
from bot.consts.texts import MENU_TEXT

BALANCES_BUTTONS = ['demo', 'general']


def select_balance_menu(balances: dict):
    text = MENU_TEXT.format(balances=balances_text(balances))
    kb = _keyboard()
    return text, kb


def _keyboard():
    balances_buttons = [
        [InlineKeyboardButton(text=f"{get_balance_icon(balance_type)}{balance_type}",
                              callback_data=f"set_balance_type_{balance_type}")]
        for balance_type in BALANCES_BUTTONS
    ]

    kb = [
        *balances_buttons,
        [
            InlineKeyboardButton(text='‹ Назад', callback_data="all_games"),
            InlineKeyboardButton(text='Правила', callback_data="rules")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
