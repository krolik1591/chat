from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.menus.main_menus.language_menu import LANGUAGES


def spam_language_menu():
    text = _('ADMIN_SPAM_LANGUAGE_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    settings_btns = [
        [InlineKeyboardButton(text=LANGUAGES[lang], callback_data="spam_lang" + lang)]
        for lang in LANGUAGES
    ]

    kb = [
        *settings_btns,
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="spam_type")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
