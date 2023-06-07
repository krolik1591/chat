from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.handlers.states import Games
from bot.menus.utils import balances_text


def select_game_menu(balances: dict):
    text = _('MENU_TEXT').format(balances=balances_text(balances))
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
        Games.CASINO: _("SELECT_GAME_BTN_CASINO"),
        Games.CUBE: _("SELECT_GAME_BTN_CUBE"),
        Games.BASKET: _("SELECT_GAME_BTN_BASKET"),
        Games.DARTS: _("SELECT_GAME_BTN_DARTS"),
        Games.BOWLING: _("SELECT_GAME_BTN_BOWLING"),
        Games.FOOTBALL: _("SELECT_GAME_BTN_FOOTBALL"),
        Games.MINES: _("SELECT_GAME_BTN_MINES"),
        Games.CUEFA: _("SELECT_GAME_BTN_CUEFA"),
    }

    games = [[
        InlineKeyboardButton(text=GAME_NAMES[game_key], callback_data="set_game_" + game_key)
        for game_key in row
    ] for row in GAMES]

    kb = [
        *games,
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
