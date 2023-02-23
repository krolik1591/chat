from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import MENU_TEXT


def main_or_demo_balance(balances: dict):
    balances_text = '\n'.join([balance_text(i) for i in balances.values()])
    text = MENU_TEXT.format(balances=balances_text)
    kb = _keyboard()

    return text, kb

# InlineKeyboardButton(text='?', callback_data=str(i)) for i in range(5)

def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Грати на TON', callback_data="2")
        ],
        [
            InlineKeyboardButton(text='DEMO', callback_data="1")
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data="all_games"),
            InlineKeyboardButton(text='Правила', callback_data="rules")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
