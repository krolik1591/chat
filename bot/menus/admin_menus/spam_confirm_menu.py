from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def approve_spam_msg():
    text = _('ADMIN_SPAM_CONFIRM_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_("ADMIN_SPAM_CONFIRM_MENU_BTN_APPROVE"), callback_data="spam_sending_approved"),
            InlineKeyboardButton(text=_("ADMIN_SPAM_CONFIRM_MENU_BTN_DENIED"), callback_data="spam_sending_denied")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
