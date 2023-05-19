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
            InlineKeyboardButton(text='🍀 Колесо фортуни', callback_data="wheel_of_fortune"),
        ],
        [
            InlineKeyboardButton(text=_('CABINET_MENU_BTN_DEPOSIT'), callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text='Аккаунт', callback_data="my_account"),
            InlineKeyboardButton(text=_('SETTING_BTN_CHANGE_LANG'), callback_data="change_lang"),

        ],
        [
            InlineKeyboardButton(text='Гайди', callback_data="guides"),
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_SUPPORT'), callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
