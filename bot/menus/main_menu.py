from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text
from aiogram.utils.i18n import gettext as _


def main_menu(balances: dict, lang):
    text = _('MENU_TEXT').format(balances=balances_text(balances))
    kb = _keyboard(lang)

    return text, kb


def _keyboard(lang):
    kb = [
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_GAMES'), callback_data="all_games"),
        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_WHEEL_OF_FORTUNE'), callback_data="wheel_of_fortune"),
        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_DEPOSIT'), callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text=_('MAIN_NEMU_BTN_ACCOUNT'), callback_data="my_account"),
            InlineKeyboardButton(text=_('MAIN_BTN_CHANGE_LANG').format(lang=lang), callback_data="change_lang"),

        ],
        [
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_GUIDES'), callback_data="guides"),
            InlineKeyboardButton(text=_('MAIN_MENU_BTN_SUPPORT'), callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
