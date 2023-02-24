from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import MENU_TEXT


def main_or_demo_balance(tokens, balances: dict):
    balances_text = '\n'.join([balance_text(i) for i in balances.values()])
    text = MENU_TEXT.format(balances=balances_text)
    # text = "Обирай свого бійця:"
    kb = _keyboard(tokens)

    return text, kb


# InlineKeyboardButton(text='?', callback_data=str(i)) for i in range(5)

def _keyboard(tokens):

    tokens_buttons = [
        [InlineKeyboardButton(text=f"{token.icon}{token.name}", callback_data=f"token_{token.id}")]
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
