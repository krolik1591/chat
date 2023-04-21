from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import BALANCE_TEXT
from bot.utils.rounding import round_down


def kb_del_msg():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='OK', callback_data="delete_message")
    ]])


def balances_text(balances):
    return '\n'.join([balance_text(i) for i in balances.values()])


def balance_text(item):
    name = item['name'].upper()  # todo use i18n to name
    amount = item['amount']
    round_amount = round_down(amount, 2)
    return BALANCE_TEXT.format(
        icon=item['icon'], name=name, amount=round_amount)

