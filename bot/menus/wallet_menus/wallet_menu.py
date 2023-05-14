from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts.const import TON_INITIALISATION_FEE
from bot.menus.utils import balances_text
from bot.consts.texts import WALLET_MENU_TEXT


def wallet_menu(balances: dict, token_price):
    text = WALLET_MENU_TEXT.format(balances=balances_text(balances),
                                   token_price=token_price, init_pay_ton=TON_INITIALISATION_FEE)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='📥 Поповнити', callback_data="replenish"),
            InlineKeyboardButton(text='📤 Вивести', callback_data="withdraw")
        ],
        [InlineKeyboardButton(text='💳 Як придбати TON?', callback_data="how_to_buy")],
        [InlineKeyboardButton(text='‹ Меню', callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
