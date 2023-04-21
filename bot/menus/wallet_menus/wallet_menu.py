from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import INIT_PAY_TON
from bot.menus.utils import balances_text
from bot.texts import DEPOSIT_MENU_TEXT


def wallet_menu(balances: dict, token_price):
    text = DEPOSIT_MENU_TEXT.format(balances=balances_text(balances),
                                    token_price=token_price, init_pay_ton=INIT_PAY_TON)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='📥 Поповнити', callback_data="replenish"),
            InlineKeyboardButton(text='📤 Вивести', callback_data="withdraw")
        ],
        [InlineKeyboardButton(text='💳 Як придбати TON?', callback_data="how_to_buy")],
        [InlineKeyboardButton(text='Меню', callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
