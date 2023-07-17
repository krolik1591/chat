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


def my_promo_code_menu(sum_bets, balance_promo, ticket_promo):
    if balance_promo is None:
        min_wager = '✅'
        if ticket_promo.deposited_wager is None:
            wager = _("PROMOCODES_MENU_NEED_WOF_WIN")
            bonus = str(ticket_promo.promocode.bonus) + ' 🎟'
        else:
            wager = f"{sum_bets}/{ticket_promo.deposited_wager}" if sum_bets < ticket_promo.deposited_wager else "✅"
            bonus = ticket_promo.deposited_bonus

        text = _('PROMOCODES_MENU_MY_PROMO_CODES_TEXT').format(min_wager=min_wager, wager=wager, bonus=bonus,
                                                               active_promo=ticket_promo.promo_name_id)

    elif ticket_promo is None:
        if balance_promo.deposited_bonus is None:
            min_wager = _("PROMOCODES_MENU_NEED_DEPOSIT_TEXT")
            wager = min_wager
            bonus = min_wager
        else:
            min_wager = f'{sum_bets}/{balance_promo.deposited_min_wager}' if sum_bets < balance_promo.deposited_min_wager else "✅"
            wager = f'{sum_bets}/{balance_promo.deposited_wager}' if sum_bets < balance_promo.deposited_wager else "✅"
            bonus = balance_promo.deposited_bonus

        text = _('PROMOCODES_MENU_MY_PROMO_CODES_TEXT').format(min_wager=min_wager, wager=wager, bonus=bonus,
                                                               active_promo=balance_promo.promo_name_id)

    else:
        balance_bonus = 0
        bonus_tickets = 0

        if balance_promo.deposited_bonus is None and ticket_promo.deposited_bonus is None:
            sum_bonus = _("PROMOCODES_MENU_WAIT_FOR_WOF_OR_REPLENISH_BALANCE")
            min_wager = sum_bonus
            wager = sum_bonus

        elif balance_promo.deposited_bonus is None:
            sum_bonus = ticket_promo.deposited_bonus
            min_wager = '✅'
            wager = f'{sum_bets}/{ticket_promo.deposited_wager}' if sum_bets < ticket_promo.deposited_wager else "✅"
            bonus_tickets = ticket_promo.promocode.bonus

        elif ticket_promo.deposited_bonus is None:
            sum_bonus = balance_promo.deposited_bonus
            min_wager = f'{sum_bets}/{balance_promo.deposited_min_wager}' if sum_bets < balance_promo.deposited_min_wager else "✅"
            wager = f'{sum_bets}/{balance_promo.deposited_wager}' if sum_bets < balance_promo.deposited_wager else "✅"
            balance_bonus = balance_promo.deposited_bonus
            bonus_tickets = ticket_promo.promocode.bonus or 0

        else:
            sum_bonus = balance_promo.deposited_bonus + ticket_promo.deposited_bonus
            min_wager = f'{sum_bets}/{balance_promo.deposited_min_wager}' if sum_bets < balance_promo.deposited_min_wager else "✅"
            wager = f'{sum_bets}/{balance_promo.deposited_wager + ticket_promo.deposited_wager}' \
                if sum_bets < balance_promo.deposited_wager + ticket_promo.deposited_wager else "✅"
            balance_bonus = balance_promo.deposited_bonus
            bonus_tickets = ticket_promo.promocode.bonus

        text = _("PROMOCODES_MENU_MY_PROMO_CODES_2_CODES_TEXT").format(
            balance_promo_name=balance_promo.promo_name_id, ticket_promo_name=ticket_promo.promo_name_id,
            text1=min_wager, text2=wager, balance_bonus=balance_bonus, bonus_tickets=bonus_tickets, sum_bonus=sum_bonus)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_CLAIM_REWARD_BTN"), callback_data="claim_reward")],
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_DECLINE_PROMO_CODE_BTN"), callback_data="decline_promo_code")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")]
    ])

    return text, kb


# def two_active_promo_code_text(sum_bets, balance_promo, ticket_promo, bonus_tickets):
#     if bonus_tickets is None:
#         bonus_tickets = 0
#
#     if balance_promo.bonus is None and ticket_promo.bonus is None:
#         sum_bonus = _("PROMOCODES_MENU_WAIT_FOR_WOF_OR_REPLENISH_BALANCE")
#         text1 = sum_bonus
#         text2 = sum_bonus
#         balance_bonus = 0
#
#     elif balance_promo.bonus is None:
#         sum_bonus = ticket_promo.bonus
#         text1 = '✅'
#         text2 = f'{sum_bets}/{ticket_promo.wager}' if sum_bets < balance_promo.wager else "✅"
#         balance_bonus = 0
#
#     elif ticket_promo.bonus is None:
#         sum_bonus = balance_promo.bonus
#         text1 = f'{sum_bets}/{balance_promo.min_wager}' if sum_bets < balance_promo.min_wager else "✅"
#         text2 = f'{sum_bets}/{balance_promo.wager}' if sum_bets < balance_promo.wager else "✅"
#         balance_bonus = balance_promo.bonus
#
#     else:
#         sum_bonus = balance_promo.bonus + ticket_promo.bonus
#         text1 = f'{sum_bets}/{balance_promo.min_wager}' if sum_bets < balance_promo.min_wager else "✅"
#         text2 = f'{sum_bets}/{balance_promo.wager + ticket_promo.wager}' \
#             if sum_bets < balance_promo.wager + ticket_promo.wager else "✅"
#         balance_bonus = balance_promo.bonus
#
#     text = _("PROMOCODES_MENU_MY_PROMO_CODES_2_CODES_TEXT").format(
#         balance_promo_name=balance_promo.promo_name, ticket_promo_name=ticket_promo.promo_name, sum_bonus=sum_bonus,
#         text1=text1, text2=text2, balance_bonus=balance_bonus, bonus_tickets=bonus_tickets)
#
#     return text
