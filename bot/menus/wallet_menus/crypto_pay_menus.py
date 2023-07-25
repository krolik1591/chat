from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def crypto_pay_menu(general_coin_amount=None, prices=None):
    print(prices)
    if not general_coin_amount:
        text = _('PROMOCODES_MENU_CRYPRO_PAY_TEXT').format()
    else:
        text = _('PROMOCODES_MENU_CRYPTO_PAY_PRICE_TEXT')
    kb_buttons = []

    if general_coin_amount:
        kb_buttons.append([InlineKeyboardButton(text=_("CRYPTO_PAY_TON_BTN").format(price=prices['ton']), callback_data="crypto_pay_TON")])
        kb_buttons.append([InlineKeyboardButton(text=_("CRYPTO_PAY_BTC_BTN").format(price=prices['btc']), callback_data="crypto_pay_BTC")])
        kb_buttons.append([InlineKeyboardButton(text=_("CRYPTO_PAY_ETH_BTN").format(price=prices['eth']), callback_data="crypto_pay_ETH")])

    kb_buttons.append([InlineKeyboardButton(text=_("BTN_BACK"), callback_data="wallet_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    return text, kb

# def amount_for_crypto_payment_menu(payment_coin):
#     text = _('CRYPTO_PAY_ENTER_AMOUNT_TEXT').format(payment_coin=payment_coin)
#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text=_("CRYPTO_PAY_COIN_ACCEPTED"), callback_data="accepted_crypto_coin")],
#         [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="crypto_pay")]
#     ])
#
#     return text, kb
