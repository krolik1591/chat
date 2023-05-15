from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.i18n import gettext as _

from bot.consts.texts import BALANCE_TEXT, PROMO_FUNDS_ICON, TON_FUNDS_ICON, DEMO_FUNDS_ICON
from bot.utils.rounding import round_down


def kb_del_msg():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='OK', callback_data="delete_message")
    ]])


def balances_text(balances):
    return '\n'.join([balance_text(i) for i in balances.items()])


def balance_text(item):
    type_, amount = item
    return BALANCE_TEXT.format(
        icon=get_balance_icon(type_),
        name=get_balance_name(item),
        amount=round_down(amount, 2)
    )


def get_balance_name(item):
    BALANCES_NAMES = {
        'demo': _('SELECT_BALANCE_BTN_DEMO'),
        'promo': _('SELECT_BALANCE_BTN_PROMO'),
        'general': _('SELECT_BALANCE_BTN_GENERAL')
    }
    return BALANCES_NAMES[item]


BALANCE_ICONS = {
    'demo': DEMO_FUNDS_ICON,
    'general': TON_FUNDS_ICON,
    'promo': PROMO_FUNDS_ICON,
}


def get_balance_icon(balance_type):
    return BALANCE_ICONS[balance_type]
