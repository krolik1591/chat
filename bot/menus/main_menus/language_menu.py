from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts


def language_menu():
    text = texts.LANGUAGE_TEXT
    kb = _keyboard()
    return text, kb

LANGUAGES = {
    'uk': 'українська',
    'en': 'english',
}

def _keyboard():
    settings_btns = [
        [InlineKeyboardButton(text=LANGUAGES[lang], callback_data="new_lang" + lang)]
        for lang in LANGUAGES
    ]

    kb = [
        *settings_btns,
        [InlineKeyboardButton(text=texts.BTN_BACK, callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
