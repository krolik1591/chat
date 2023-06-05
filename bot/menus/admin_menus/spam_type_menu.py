from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def spam_type_menu():
    text = _('ADMIN_SPAM_TYPE_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_("ADMIN_SPAM_TYPE_MENU_BTN_ALL_USERS"), callback_data="spam_type"),
        ],
        [
            InlineKeyboardButton(text=_("ADMIN_SPAM_TYPE_MENU_BTN_FOR_ID"), callback_data="spam_type"),
        ],
        [
            InlineKeyboardButton(text=_("BTN_BACK"), callback_data="admin_menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
