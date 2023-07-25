from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def crypto_pay_menu(general_coin_amount=None, prices=None):
    if not general_coin_amount:
        text = _('PROMOCODES_MENU_CRYPRO_PAY_TEXT').format()
    else:
        text = _('PROMOCODES_MENU_CRYPTO_PAY_PRICE_TEXT')
    kb_buttons = []
    if general_coin_amount:
        for coin, amount in prices.items():
            kb_buttons.append([InlineKeyboardButton(text=_(f"CRYPTO_PAY_{coin}_BTN").format(price=round(amount, 5)),
                                                    callback_data=f"crypto_pay_{coin}|{amount}")])

    kb_buttons.append([InlineKeyboardButton(text=_("BTN_BACK"), callback_data="replenish")])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    return text, kb


def get_link_to_deposit_menu(coin, price, link, deposit_amount):
    text = _('CRYPTO_PAY_GET_LINK_TO_DEP_TEXT').format(coin=coin, price=price, link=link, deposit_amount=deposit_amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("CRYPTO_PAY_COIN_ACCEPTED"), callback_data="wallet_menu")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="replenish")]
    ])

    return text, kb


def tokens():
    bnb = _("CRYPTO_PAY_BNB_BTN")
    busd = _("CRYPTO_PAY_BUSD_BTN")
    usdc = _("CRYPTO_PAY_USDC_BTN")
    usdt = _("CRYPTO_PAY_USDT_BTN")
    trx = _("CRYPTO_PAY_TRX_BTN")
    ton = _("CRYPTO_PAY_TON_BTN")
    btc = _("CRYPTO_PAY_BTC_BTN")
    eth = _("CRYPTO_PAY_ETH_BTN")
