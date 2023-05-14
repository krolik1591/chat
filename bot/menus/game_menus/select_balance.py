from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.menus.utils import balances_text, get_balance_icon

BALANCES_BUTTONS = ['demo', 'general']


def select_balance_menu(balances: dict):
    text = _('MENU_TEXT').format(balances=balances_text(balances))
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
