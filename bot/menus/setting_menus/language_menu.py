from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.i18n import gettext as _


def language_menu():
    text = _('LANGUAGE_TEXT')
    kb = _keyboard()

    return text, kb


LANGUAGES = {
    'ua': '🇺🇦 Українська',
    'en': '🇺🇸 English',
    'ru': '💩 русский'
}


def _keyboard():
    settings_btns = [
        [InlineKeyboardButton(text=LANGUAGES[lang], callback_data="new_lang" + lang)]
        for lang in LANGUAGES
    ]

    kb = [
        *settings_btns,
        [InlineKeyboardButton(text=_('BACK'), callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
