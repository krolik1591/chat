from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def crypto_pay_menu():
    text = _('PROMOCODES_MENU_CRYPRO_PAY_TEXT').format()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("CRYPTO_PAY_TON_BTN"), callback_data="crypto_pay_TON")],
        [InlineKeyboardButton(text=_("CRYPTO_PAY_BTC_BTN"), callback_data="crypto_pay_BTC")],
        [InlineKeyboardButton(text=_("CRYPTO_PAY_ETH_BTN"), callback_data="crypto_pay_ETH")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="wallet_menu")]
    ])

    return text, kb
