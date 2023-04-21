from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import BALANCE_TEXT, TON_FUNDS_ICON, DEMO_FUNDS_ICON
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
        name=type_.upper(),
        amount=round_down(amount, 2)
    )


BALANCE_ICONS = {
    'demo': DEMO_FUNDS_ICON,
    'general': TON_FUNDS_ICON,
    'promo': "🎁",
}


def get_balance_icon(balance_type):
    return BALANCE_ICONS[balance_type]
