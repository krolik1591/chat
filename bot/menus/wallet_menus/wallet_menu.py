from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.consts.const import TON_INITIALISATION_FEE
from bot.menus.utils import balances_text


def wallet_menu(balances: dict, token_price):
    text = _('WALLET_MENU_TEXT').format(balances=balances_text(balances),
                                        token_price=token_price, init_pay_ton=TON_INITIALISATION_FEE)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('WALLET_MENU_BTN_DEPOSIT'), callback_data="replenish"),
            InlineKeyboardButton(text=_('WALLET_MENU_BTN_WITHDRAW'), callback_data="withdraw")
        ],
        [InlineKeyboardButton(text=_('WALLET_MENU_BTN_HOW_TO_BUY'), callback_data="how_to_buy")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
