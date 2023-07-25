from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.consts.const import TON_INITIALISATION_FEE
from bot.menus.utils import kb_del_msg
from bot.utils.rounding import round_down


def deposit_account_initiation(is_successful_inited):
    if is_successful_inited:
        text = _('DEPOSIT_ACCOUNT_INITIATED').format(init_pay_ton=TON_INITIALISATION_FEE)
    else:
        text = _('DEPOSIT_INITIATION_ERROR').format(init_pay_ton=TON_INITIALISATION_FEE)

    return text, kb_del_msg()


def successful_deposit_menu(amount):
    amount = round_down(amount, 2)
    text = _('DEPOSIT_SUCCESSFUL').format(amount=amount)
    return text, kb_del_msg()


def deposit_menu(wallet_address):
    text = _('DEPOSIT_MENU_TEXT').format(wallet_address=wallet_address)
    kb = _replenish_menu_keyboard(wallet_address)

    return text, kb


def _replenish_menu_keyboard(wallet_address):
    kb = [
        [InlineKeyboardButton(text=_('DEPOSIT_MENU_BTN_OPEN_TONKEEPER'),
                              url=f"https://app.tonkeeper.com/transfer/{wallet_address}")],
        [InlineKeyboardButton(text=_('DEPOSIT_MENU_BTN_OPEN_TONKEEPER2'),
                              url=f"https://app.tonkeeper.com/transfer/{wallet_address}")],
        [InlineKeyboardButton(text=_('DEPOSIT_MENU_BTN_OPEN_CRYPTO_PAY'), callback_data="crypto_pay")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wallet_menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
