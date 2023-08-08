from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts
from bot.menus.utils import balances_text, get_balance_icon, get_balance_name

BALANCES_BUTTONS = ['demo', 'general', 'promo']


def select_balance_menu(balances: dict):
    text = texts.MENU_TEXT.format(balances=balances_text(balances))
    kb = _keyboard()
    return text, kb


def _keyboard():
    balances_buttons = [
        [InlineKeyboardButton(text=f"{get_balance_icon(balance_type)}{get_balance_name(balance_type)}",
                              callback_data=f"set_balance_type_{balance_type}")]
        for balance_type in BALANCES_BUTTONS
    ]

    kb = [
        *balances_buttons,
        [
            InlineKeyboardButton(text=texts.BTN_BACK, callback_data="all_games"),
            InlineKeyboardButton(text=texts.SELECT_BALANCE_BTN_RULES, callback_data="rules")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)