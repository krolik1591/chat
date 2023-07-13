from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def promo_code_menu():
    text = _('PROMOCODES_MENU_PROMO_CODES_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("ACCOUNT_MENU_ACTIVE_PROMO_CODE_BTN"), callback_data="active_promo_code")],
        [InlineKeyboardButton(text=_("ACCOUNT_MENU_MY_PROMO_CODE_BTN"), callback_data="my_promo_codes")],
        [InlineKeyboardButton(text=_("ACCOUNT_MENU_PROMO_CODES_AVAILABLE_BTN"), callback_data="promo_code_available")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="my_account")]
    ])

    return text, kb


def active_promo_code_menu(text):
    text = _('PROMOCODES_MENU_ACTIVE_PROMO_CODES_TEXT').format(text=text)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")]
    ])

    return text, kb


def my_promo_code_menu(sum_bets, min_wager, wager, active_promo):
    if sum_bets is None:
        sum_bets = 0

    text1 = f'{sum_bets}/{min_wager}'
    text2 = f'{sum_bets}/{wager}'

    if min_wager is None or wager is None:
        text1 = _("PROMOCODES_MENU_NEED_DEPOSIT_TEXT")
        text2 = text1

    text = _('PROMOCODES_MENU_MY_PROMO_CODES_TEXT').format(text1=text1, text2=text2, active_promo=active_promo)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_CLAIM_REWARD_BTN"), callback_data="claim_reward")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")]
    ])

    return text, kb
