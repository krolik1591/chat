from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts
from bot.menus.utils import balances_text


def main_menu(balances: dict, lang):
    text = texts.MENU_TEXT.format(balances=balances_text(balances))
    kb = _keyboard(lang)

    return text, kb


def _keyboard(lang):
    kb = [
        [
            InlineKeyboardButton(text=texts.MAIN_MENU_BTN_GAMES, callback_data="all_games"),
        ],
        [
            InlineKeyboardButton(text=texts.MAIN_MENU_BTN_WHEEL_OF_FORTUNE, callback_data="wheel_of_fortune"),
        ],
        [
            InlineKeyboardButton(text=texts.MAIN_MENU_BTN_DEPOSIT, callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text=texts.MAIN_NEMU_BTN_ACCOUNT, callback_data="my_account"),
            InlineKeyboardButton(text=texts.MAIN_BTN_CHANGE_LANG.format(lang=lang), callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text=texts.MAIN_MENU_BTN_GUIDES, callback_data="guides"),
            InlineKeyboardButton(text=texts.MAIN_MENU_BTN_SUPPORT, callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
