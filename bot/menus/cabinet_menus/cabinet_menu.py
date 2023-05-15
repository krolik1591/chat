from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.i18n import gettext as _


def cabinet_menu():
    text = _('CABINET_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('CABINET_MENU_BTN_DEPOSIT'), callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text=_('CABINET_MENU_BTN_REFERRALS'), callback_data="referrals_menu")
        ],
        [
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
