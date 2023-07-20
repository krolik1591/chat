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


def my_promo_code_menu(sum_bets_min_wager, balance_promo, ticket_promo, sum_bets_wager):
    def format_wager(sum_bets, deposited_wager):
        return f"{sum_bets}/{deposited_wager}" if sum_bets < deposited_wager else "✅"

    def format_promo_names():
        r = []
        if balance_promo:
            r.append(_("MY_PROMO_CODE_MENU_ACTIVE_PROMO_BALANCE").format(balance_bonus=balance_promo.promo_name_id))
        if ticket_promo:
            r.append(_("MY_PROMO_CODE_MENU_ACTIVE_PROMO_TICKET").format(bonus_tickets=ticket_promo.promo_name_id))
        return ' | '.join(r)

    def format_wof_promo():
        min_wager = '✅'
        if ticket_promo.deposited_wager == 0:
            wager = _("PROMOCODES_MENU_NEED_WOF_WIN")
            bonus = str(ticket_promo.promocode.bonus) + ' 🎟'
        else:
            wager = format_wager(sum_bets_wager, ticket_promo.deposited_wager)
            bonus = ticket_promo.deposited_bonus

        return min_wager, wager, bonus

    def format_balance_promo():
        if balance_promo.deposited_bonus == 0:
            t = _("PROMOCODES_MENU_NEED_DEPOSIT_TEXT")
            return t, t, t

        min_wager = format_wager(sum_bets_min_wager, balance_promo.deposited_min_wager)
        wager = format_wager(sum_bets_wager, balance_promo.deposited_wager)
        bonus = balance_promo.deposited_bonus

        return min_wager, wager, bonus

    def format_both_promos():
        sum_bonus = balance_promo.deposited_bonus + ticket_promo.deposited_bonus
        min_wager = format_wager(sum_bets_min_wager, balance_promo.deposited_min_wager)
        wager = format_wager(sum_bets_wager, balance_promo.deposited_wager + ticket_promo.deposited_wager)

        return min_wager, wager, sum_bonus

    balance_bonus = balance_promo.deposited_bonus if balance_promo else 0
    bonus_tickets = ticket_promo.promocode.bonus if ticket_promo else 0

    if balance_promo and ticket_promo:
        if balance_bonus == 0 and ticket_promo.deposited_bonus == 0:
            t = _("PROMOCODES_MENU_WAIT_FOR_WOF_OR_REPLENISH_BALANCE")
            min_wager, wager, bonus = t, t, t
        else:
            min_wager, wager, bonus = format_both_promos()
    elif balance_promo:
        min_wager, wager, bonus = format_balance_promo()
    elif ticket_promo:
        min_wager, wager, bonus = format_wof_promo()
    else:
        raise Exception("kek")

    active_promo_codes = format_promo_names()
    text = _("PROMOCODES_MENU_MY_PROMO_CODES_2_CODES_TEXT").format(
        active_promocodes=active_promo_codes,
        min_wager=min_wager, wager=wager, sum_bonus=bonus,
        balance_bonus=balance_bonus, bonus_tickets=bonus_tickets)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_CLAIM_REWARD_BTN"), callback_data="claim_reward")],
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_DECLINE_PROMO_CODE_BTN"), callback_data="approve_decline_promo_code")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")]
    ])

    return text, kb


def approve_decline_promo_code_menu():
    text = _('PROMOCODES_MENU_APPROVE_DECLINE_PROMO_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_APPROVE_DECLINE_PROMO_BTN"), callback_data="decline_promo_code")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")],
    ])

    return text, kb


def approve_activation_balance_promo(ticket_promo_name, balance_promo_name):
    text = _('PROMOCODES_MENU_APPROVE_ACTIVATE_BALANCE_PROMO_TEXT').format(ticket_promo_name=ticket_promo_name,
                                                                           balance_promo_name=balance_promo_name)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("PROMOCODES_MENU_APPROVE_ACTIVATE_BALANCE_PROMO_BTN"),
                              callback_data="activate_promo_balance")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="promo_codes")],
    ])

    return text, kb
