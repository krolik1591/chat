from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers.states import Games
from bot.menus.main_menu import balance_text
from bot.texts import MENU_TEXT


def game_choice_menu(balances: dict):
    balances_text = '\n'.join([balance_text(i) for i in balances.values()])
    text = MENU_TEXT.format(balances=balances_text)
    kb = _keyboard()

    return text, kb


GAMES = [
    [Games.CASINO, Games.CUBE],
    [Games.BASKET, Games.DARTS],
    [Games.BOWLING, Games.FOOTBALL],
    [Games.MINES, Games.CUEFA],
]

# todo i18n
GAME_NAMES = {
    Games.CASINO: "Слоти",
    Games.CUBE: "Кубік",
    Games.BASKET: "Баскет",
    Games.DARTS: "Дартс",
    Games.BOWLING: "Боулінг",
    Games.FOOTBALL: "Футбол",
    Games.MINES: "Міни",
    Games.CUEFA: "Цу-Е-Фа",
}


def _keyboard():
    games = [[
        InlineKeyboardButton(text=GAME_NAMES[game_key], callback_data="set_game_" + game_key)
        for game_key in row
    ] for row in GAMES]

    kb = [
        *games,
        [InlineKeyboardButton(text='Назад', callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
