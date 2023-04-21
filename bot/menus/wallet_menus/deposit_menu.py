from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import TON_INITIALISATION_FEE
from bot.menus.utils import kb_del_msg
from bot.texts import DEPOSIT_INITIATION_ERROR, DEPOSIT_ACCOUNT_INITIATED, SUCCESSFUL_REPLENISH_MENU, \
    REPLENISH_MENU_TEXT
from bot.utils.rounding import round_down


def deposit_account_initiation(is_successful_inited):
    if is_successful_inited:
        text = DEPOSIT_ACCOUNT_INITIATED.format(init_pay_ton=TON_INITIALISATION_FEE)
    else:
        text = DEPOSIT_INITIATION_ERROR.format(init_pay_ton=TON_INITIALISATION_FEE)

    return text, kb_del_msg()


def successful_deposit_menu(amount):
    amount = round_down(amount, 2)
    text = SUCCESSFUL_REPLENISH_MENU.format(amount=amount)
    return text, kb_del_msg()


def deposit_menu(wallet_address):
    text = REPLENISH_MENU_TEXT.format(wallet_address=wallet_address)
    kb = _replenish_menu_keyboard(wallet_address)

    return text, kb


def _replenish_menu_keyboard(wallet_address):
    kb = [
        [InlineKeyboardButton(text='Відкрити Tonkeeper', url=f"https://app.tonkeeper.com/transfer/{wallet_address}")],
        [InlineKeyboardButton(text='Todo link', url=f"https://app.tonkeeper.com/transfer/{wallet_address}")],
        [
            InlineKeyboardButton(text='Мій гаманець', callback_data="wallet_menu"),
            InlineKeyboardButton(text='Оновити баланс', callback_data="ton_check")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
