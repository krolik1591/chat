from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.consts.balance import PROMO_FUNDS_ICON, TON_FUNDS_ICON


def wheel_of_fortune_menu(ticket_cost, date_end, user_tickets, wof_win):
    if not wof_win['promo']:
        display_win = str(wof_win['general']) + ' ' + TON_FUNDS_ICON
    elif not wof_win['general']:
        display_win = str(wof_win['promo']) + ' ' + PROMO_FUNDS_ICON
    else:
        display_win = f"{str(wof_win['general']) + ' ' + TON_FUNDS_ICON} | " \
                      f"{str(wof_win['promo']) + ' ' + PROMO_FUNDS_ICON}"

    text = _('WHEEL_OF_FORTUNE_TEXT_MENU').format(ticket_cost=ticket_cost, date_end=date_end, user_tickets=user_tickets,
                                                  wof_win=display_win)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_BUY_TICKET'), callback_data="buy_ticket")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_MY_NUMBERS'), callback_data="my_numbers")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_BUY_TICKET_CHECK_MY_STATUS'), callback_data="check_status")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_SPIN_RESULT'), callback_data="spin_result")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_CLAIM_WIN'), callback_data="claim_wof_reward")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")],
    ])

    return text, kb


def wheel_of_fortune_doesnt_exist_menu(user_wof_win):
    text = _('WHEEL_OF_FORTUNE_DOESNT_EXIST_TEXT_MENU').format(user_wof_win=user_wof_win)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_SPIN_RESULT'), callback_data="spin_result")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_CLAIM_WIN'), callback_data="claim_wof_reward")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")],
    ])

    return text, kb


def buy_ticket_menu(wof_info, user_balance, user_tickets):
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost
    ticket_cost = wof_info.ticket_cost
    text = _('WOF_MENU_BUY_TICKET_TEXT').format(how_much_tickets_can_buy=how_much_tickets_can_buy,
                                                user_balance=user_balance, ticket_cost=ticket_cost,
                                                user_tickets=user_tickets)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_TICKET_MENU_SELECT_NUM'), callback_data="buy_selected_num")],
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_TICKET_MENU_RANDOM_NUM'), callback_data="buy_random_num")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wheel_of_fortune")],
    ])

    return text, kb


def buy_selected_num_menu(wof_info, user_balance, user_tickets, ticket_num=''):
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost
    ticket_cost = wof_info.ticket_cost
    text = _('WOF_MENU_BUY_SELECTED_TICKET_TEXT').format(how_much_tickets_can_buy=how_much_tickets_can_buy,
                                                         user_balance=user_balance, ticket_cost=ticket_cost,
                                                         user_tickets=user_tickets,
                                                         ticket_num=ticket_num.zfill(7) if ticket_num else '')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_SELECTED_NUM_MENU'), callback_data="buy_ticket_selected_num")]
        if ticket_num else [],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="buy_ticket")],
    ])

    return text, kb


def buy_random_num_menu(wof_info, user_balance, user_tickets, ticket_count=10):
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost
    ticket_cost = wof_info.ticket_cost
    text = _('WOF_MENU_BUY_RANDOM_TICKET_TEXT').format(how_much_tickets_can_buy=how_much_tickets_can_buy,
                                                       user_balance=user_balance, ticket_cost=ticket_cost,
                                                       user_tickets=user_tickets)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='-', callback_data="change_tickets_count_-"),
         InlineKeyboardButton(text=ticket_count, callback_data="display_count_ticket"),
         InlineKeyboardButton(text='+', callback_data="change_tickets_count_+")],
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_RANDOM_NUM_MENU'), callback_data="buy_ticket_random_num")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="buy_ticket")],
    ])

    return text, kb


def my_numbers_menu(selected_tickets, random_tickets):
    text = _('WHEEL_OF_FORTUNE_MY_NUMBERS_TEXT').format(selected_tickets=selected_tickets,
                                                        random_tickets=random_tickets,
                                                        all_tickets=selected_tickets + random_tickets)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_MY_NUMBERS_BTN_DISPLAY_SELECTED'), callback_data="display_tickets_selected")],
        [InlineKeyboardButton(text=_('WOF_MY_NUMBERS_BTN_DISPLAY_RANDOM'), callback_data="display_tickets_random")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wheel_of_fortune")],
    ])

    return text, kb


def display_ticket_num_text_menu(tickets_text, page, pages):
    text = _('WHEEL_OF_FORTUNE_MY_NUMBERS_TEXT_1').format(tickets_text=tickets_text, page=page, pages=pages)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_PREVIOUS_TICKET_PAGE'),
                                 callback_data="ticket_page_previous"),
            InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_NEXT_TICKET_PAGE'), callback_data="ticket_page_next"),
        ],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="my_numbers")],
    ])

    return text, kb


def what_balance_withdraw_menu(wof_rewards):
    text = _('WHEEL_OF_FORTUNE_WHAT_BALANCE_WITHDRAW_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_WHAT_BALANCE_GENERAL').format(
                general_balance=str(wof_rewards['general']) + ' ' + TON_FUNDS_ICON), callback_data="claim_wof_balance_general"),
            InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_WHAT_BALANCE_PROMO').format(
                promo_balance=str(wof_rewards['promo']) + ' ' + PROMO_FUNDS_ICON), callback_data="claim_wof_balance_promo"),
        ],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wheel_of_fortune")],
    ])

    return text, kb
