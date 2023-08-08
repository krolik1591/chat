from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts
from bot.handlers.states import Games
from bot.menus.utils import balances_text


def select_game_menu(balances: dict):
    text = texts.MENU_TEXT.format(balances=balances_text(balances))
    kb = _keyboard()

    return text, kb


GAMES = [
    [Games.CASINO],
    [Games.CUBE],
    [Games.BASKET, Games.DARTS],
    [Games.BOWLING, Games.FOOTBALL],
    [Games.MINES, Games.CUEFA],
]


def _keyboard():
    GAME_NAMES = {
        Games.CASINO: texts.SELECT_GAME_BTN_CASINO,
        Games.CUBE: texts.SELECT_GAME_BTN_CUBE,
        Games.BASKET: texts.SELECT_GAME_BTN_BASKET,
        Games.DARTS: texts.SELECT_GAME_BTN_DARTS,
        Games.BOWLING: texts.SELECT_GAME_BTN_BOWLING,
        Games.FOOTBALL: texts.SELECT_GAME_BTN_FOOTBALL,
        Games.MINES: texts.SELECT_GAME_BTN_MINES,
        Games.CUEFA: texts.SELECT_GAME_BTN_CUEFA,
    }

    games = [[
        InlineKeyboardButton(text=GAME_NAMES[game_key], callback_data="set_game_" + game_key)
        for game_key in row
    ] for row in GAMES]

    kb = [
        *games,
        [InlineKeyboardButton(text=texts.BTN_BACK, callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
