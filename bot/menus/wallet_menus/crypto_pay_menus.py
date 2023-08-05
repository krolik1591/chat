from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def crypto_pay_menu(general_coin_amount=None, prices=None, enter_amount=0):
    if not general_coin_amount:
        text = _('PROMOCODES_MENU_CRYPRO_PAY_TEXT').format()
    else:
        text = _('PROMOCODES_MENU_CRYPTO_PAY_PRICE_TEXT').format(enter_amount=enter_amount)
    kb_buttons = []
    if general_coin_amount:
        raw = []
        for coin, amount in prices.items():
            raw.append(InlineKeyboardButton(text=_(f"CRYPTO_PAY_COIN_BTN").format(price=round(amount, 5), coin=coin),
                                            callback_data=f"crypto_pay_{coin}|{amount}"))
            if len(raw) == 2:
                kb_buttons.append(raw)
                raw = []

    kb_buttons.append([InlineKeyboardButton(text=_("BTN_BACK"), callback_data="replenish")])
    kb_buttons = *kb_buttons,
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    return text, kb


def get_link_to_deposit_menu(coin_name, amount_to_invoice, link, desired_gametokens_amount):
    text = _('CRYPTO_PAY_GET_LINK_TO_DEP_TEXT').format(link=link, coin_name=coin_name,
                                                       amount_to_invoice=amount_to_invoice,
                                                       desired_gametokens_amount=desired_gametokens_amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("CRYPTO_PAY_COIN_ACCEPTED"), url=link)],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="replenish")]
    ])

    return text, kb


def warning_about_optimized_buy_gametoken():
    text = _('CRYPTO_PAY_WARNING_ABOUT_OPTIMIZED_BUY_GAMETOKEN').format()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("CRYPTO_PAY_DUNKY_CHOICE_BTN"), callback_data='dunky_choice_accept')],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="replenish")]
    ])

    return text, kb
