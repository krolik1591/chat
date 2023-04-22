from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts
from bot.consts.const import MIN_BET
from bot.handlers.states import Games
from bot.menus.utils import get_balance_icon
from bot.consts.texts import DEFAULT_BALANCE_TEXT, DEFAULT_PLAY_TEXT
from bot.utils.rounding import round_down


def bet_menu(bet, balance, balance_type, game_mode=None):
    balance = round_down(balance, 2)

    if game_mode == Games.CASINO:
        return _base_bet_menu(balance, bet, balance_type=balance_type, play_text=texts.SLOTS_PLAY_TEXT)
    if game_mode == Games.FOOTBALL:
        return _base_bet_menu(balance, bet, balance_type=balance_type, play_text=texts.FOOTBALL_PLAY_TEXT)
    if game_mode == Games.DARTS:
        return _base_bet_menu(balance, bet, balance_type=balance_type, play_text=texts.DARTS_PLAY_TEXT)

    if game_mode == Games.CUBE:
        return _base_bet_menu(balance, bet, balance_type=balance_type, play_text=texts.CUBE_PLAY_TEXT,
                              back_to='game_settings')

    return _base_bet_menu(balance, bet, balance_type=balance_type)


def _base_bet_menu(
        balance, bet, balance_type,
        text=DEFAULT_BALANCE_TEXT,
        play_text=DEFAULT_PLAY_TEXT,
        back_to='select_balance_type'
):
    balance_icon = get_balance_icon(balance_type)
    text = text.format(balance=balance, bet=bet)

    add_replenish_btn = balance_type == 'demo' and balance < MIN_BET
    kb = _keyboard(bet, balance_icon, play_text, add_replenish_btn, back_to)

    return text, kb


def _keyboard(bet, balance_icon, play_text, add_replenish_btn, back_to):
    kb = [

        *(_btn_replenish() if add_replenish_btn else []),
        [
            InlineKeyboardButton(text='-', callback_data="bet_minus"),
            InlineKeyboardButton(text=f'{bet}{balance_icon}', callback_data="bet_token_icon"),
            InlineKeyboardButton(text='+', callback_data="bet_plus")
        ],
        [
            InlineKeyboardButton(text='Мін.', callback_data="bet_min"),
            InlineKeyboardButton(text='Подвоїти', callback_data="bet_x2"),
            InlineKeyboardButton(text='Макс.', callback_data="bet_max")
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=back_to),
            InlineKeyboardButton(text=play_text, callback_data="game_play")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def _btn_replenish():
    return [[InlineKeyboardButton(text='Дай гроші', callback_data="end_money")]]
