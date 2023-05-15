from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.i18n import gettext as _


def setting_menu():
    text = _('SETTING_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('SETTING_BTN_CHANGE_LANG'), callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
