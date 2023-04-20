from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.menus.utils import kb_del_msg
from bot.texts import CUBE_MULTIPLY_BET_ERR, GAME_ERR1

GAME_ERR = {
    'low_balance_big_wish': CUBE_MULTIPLY_BET_ERR,
    1: GAME_ERR1    # user doesnt choice bet
}


def game_menu_err(err):
    text = GAME_ERR[err]

    kb = kb_del_msg()

    return text, kb
