from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.main_menu import balance_text
from bot.texts import DEPOSIT_MENU_TEXT, MENU_TEXT, REPLENISH_MENU_TEXT, WITHDRAW_MENU_TEXT1, WITHDRAW_MENU_TEXT1_1, \
    WITHDRAW_MENU_TEXT1_2, WITHDRAW_MENU_TEXT1_3, WITHDRAW_MENU_TEXT1_4, WITHDRAW_MENU_TEXT2


def withdraw_menu_err(err):
    print(err)
    if err == 1:
        text = WITHDRAW_MENU_TEXT1_1.format()
    elif err == 2:
        text = WITHDRAW_MENU_TEXT1_2.format()
    elif err == 3:
        text = WITHDRAW_MENU_TEXT1_3.format()
    elif err == 4:
        text = WITHDRAW_MENU_TEXT1_4.format()

    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)