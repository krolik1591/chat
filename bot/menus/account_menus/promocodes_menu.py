from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def promo_code_menu(promo_code):
    text = _('PROMOCODES_MENU_PROMO_CODES_TEXT').format(promo_code=promo_code)
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


def my_promo_code_menu(sum_bets, balance_promo, ticket_promo=0):
    if sum_bets is None:
        sum_bets = 0

    if ticket_promo == 0:
        text = one_active_promo_code_text(sum_bets, balance_promo)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_CLAIM_REWARD_BTN"), callback_data="claim_reward")],
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_DECLINE_PROMO_CODE_BTN"), callback_data="decline_promo_code")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")]
    ])

    return text, kb


def one_active_promo_code_text(sum_bets, balance_promo):
    if balance_promo.promo_type == "balance":
        if balance_promo.wager is None:
            text1 = _("PROMOCODES_MENU_NEED_DEPOSIT_TEXT")
            text2 = text1
            bonus = text1
        else:
            text1 = f'{sum_bets}/{balance_promo.min_wager}' if sum_bets < balance_promo.min_wager else "✅"
            text2 = f'{sum_bets}/{balance_promo.wager}' if sum_bets < balance_promo.wager else "✅"
            bonus = balance_promo.bonus

    else:  # balance_promo.promo_type == 'ticket':
        text1 = '✅'
        if balance_promo.wager is None:
            text2 = _("PROMOCODES_MENU_NEED_WOF_WIN")
            bonus = text2
        else:
            text2 = f"{sum_bets}/{balance_promo.bonus * balance_promo.wager}" if sum_bets < balance_promo.wager else "✅"
            bonus = balance_promo.bonus if balance_promo.bonus is not None else _("PROMOCODES_MENU_NEED_WOF_WIN")

    sticker = '🎁 ' if balance_promo.promo_type == 'balance' else '🎟 '
    text = _('PROMOCODES_MENU_MY_PROMO_CODES_TEXT').format(text1=text1, text2=text2, bonus=bonus,
                                                           active_promo=sticker + balance_promo.promo_name)

    return text