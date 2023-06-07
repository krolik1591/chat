from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def wheel_of_fortune_menu():
    text = _('WHEEL_OF_FORTUNE_TEXT_MENU')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_BUY_TICKET'), callback_data="buy_ticket")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_MY_NUMBERS'), callback_data="my_numbers")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_BUY_TICKET_CHECK_MY_STATUS'), callback_data="check_status")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_SPIN_RESULT'), callback_data="spin_result")],
        [InlineKeyboardButton(text=_('WHEEL_FORTUNE_BTN_CLAIM_WIN'), callback_data="claim_win")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")],
    ])

    return text, kb


def buy_ticket_menu():
    text = _('WOF_MENU_BUY_TICKET_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_TICKET_MENU_SELECT_NUM'), callback_data="buy_selected_num")],
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_TICKET_MENU_RANDOM_NUM'), callback_data="buy_random_num")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wheel_of_fortune")],
    ])

    return text, kb


def buy_selected_num_menu():
    text = _('WOF_MENU_BUY_SELECTED_TICKET_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_SELECTED_NUM_MENU'), callback_data="buy_this_num")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="buy_ticket")],
    ])

    return text, kb


def buy_random_num_menu():
    text = _('WOF_MENU_BUY_RANDOM_TICKET_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WOF_BTN_BUY_RANDOM_NUM_MENU'), callback_data="buy_this_num")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="buy_ticket")],
    ])

    return text, kb
