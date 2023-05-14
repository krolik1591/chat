from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text
from aiogram.utils.i18n import gettext as _


def main_menu(balances: dict):
    text = _('MENU_TEXT').format(balances=balances_text(balances))
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_GAMES'), callback_data="all_games"),
        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_CABINET'), callback_data="cabinet_menu")
        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_SETTINGS'), callback_data="settings")
        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_ADS'), callback_data="spam"),
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_SUPPORT'), callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
