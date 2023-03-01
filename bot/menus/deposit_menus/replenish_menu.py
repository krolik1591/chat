from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT, REPLENISH_MENU_TEXT


def replenish_menu(wallet_address):
    print(wallet_address)
    text = REPLENISH_MENU_TEXT.format(wallet_address=wallet_address)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Відкрити Tonkeeper',
                                 url="https://app.tonkeeper.com/transfer/EQC5hQd4Icr36z0GD2vlrJIFZzHGa7TWK66rMwxnVI8TQuU0")
        ],
        [
            InlineKeyboardButton(text='Відкрити TonHub',
                                 url="https://app.tonkeeper.com/transfer/EQC5hQd4Icr36z0GD2vlrJIFZzHGa7TWK66rMwxnVI8TQuU0")
        ],
        [
            InlineKeyboardButton(text='Мій гаманець', callback_data="deposit"),
            InlineKeyboardButton(text='Оновити баланс', callback_data="ton_check")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)