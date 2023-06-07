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
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="list_for_spam_approved")],
    ])

    return text, kb
