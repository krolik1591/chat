from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text
from bot.texts import MENU_TEXT


def select_token_menu(tokens, balances: dict):
    text = MENU_TEXT.format(balances=balances_text(balances))

    kb = _keyboard(tokens)

    return text, kb


def _keyboard(tokens):

    tokens_buttons = [
        [InlineKeyboardButton(text=f"{token.icon}{token.name}", callback_data=f"set_token_{token.token_id}")]
        for token in tokens
    ]

    kb = [
        *tokens_buttons,
        [
            InlineKeyboardButton(text='Назад', callback_data="all_games"),
            InlineKeyboardButton(text='Правила', callback_data="rules")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
