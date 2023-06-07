from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def admin_menu():
    text = _('ADMIN_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_("ADMIN_MENU_BTN_SPAM"), callback_data="spam_type"),
        ],
        [
            InlineKeyboardButton(text=_("ADMIN_MENU_BTN_STATISTIC"), callback_data="stat"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
