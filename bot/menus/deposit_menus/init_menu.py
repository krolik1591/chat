from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import INIT_CONDITION_FALSE, INIT_CONDITION_TRUE


def init_menu(condition, init_pay_ton):
    if condition:
        text = INIT_CONDITION_TRUE.format(init_pay_ton=init_pay_ton)
    else:
        text = INIT_CONDITION_FALSE.format(init_pay_ton=init_pay_ton)


    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)