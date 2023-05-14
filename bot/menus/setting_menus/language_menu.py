from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts.texts import LANGUAGE_TEXT


def language_menu():
    text = LANGUAGE_TEXT
    kb = _keyboard()

    return text, kb


LANGUAGES = {
    'ua': 'Українська',
    'en': 'Англійська'
}


def _keyboard():
    settings_btns = [
        [InlineKeyboardButton(text=LANGUAGES[lang], callback_data="new_lang" + lang)]
        for lang in LANGUAGES
    ]

    kb = [
        *settings_btns,
        [InlineKeyboardButton(text='‹ Назад', callback_data="settings")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
