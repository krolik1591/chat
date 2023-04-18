from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import CUBE_MULTIPLY_BET_ERR, GAME_ERR1

GAME_ERR = {
    'low_balance_big_wish': CUBE_MULTIPLY_BET_ERR,
    1: GAME_ERR1    # user doesnt choice bet
}


def game_menu_err(err):
    text = GAME_ERR[err]

    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)