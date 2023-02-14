from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.const import MIN_BET
from bot.texts import DEFAULT_BALANCE_TEXT, DEMO_FUNDS_ICON, DEFAULT_PLAY_TEXT


def game_menu_base(
        balance, bet,
        text=DEFAULT_BALANCE_TEXT,
        btns_before_bet=[],
        btns_after_bet=[],
        funds_icon=DEMO_FUNDS_ICON,
        play_text=DEFAULT_PLAY_TEXT,
):
    text = text.format(balance=balance, bet=bet)

    add_replenish_btn = bet > balance > MIN_BET
    kb = _keyboard(bet, btns_before_bet, btns_after_bet, funds_icon, play_text, add_replenish_btn)

    return text, kb


def _keyboard(
        bet,
        btns_before_bet, btns_after_bet,
        funds_icon, play_text,
        add_replenish_btn
):
    kb = [
        *(_btn_replenish() if add_replenish_btn else []),
        *btns_before_bet,
        [
            InlineKeyboardButton(text='-', callback_data="bet_minus"),
            InlineKeyboardButton(text=f'{bet}{funds_icon}', callback_data="withdraw"),
            InlineKeyboardButton(text='+', callback_data="bet_plus")
        ],
        [
            InlineKeyboardButton(text='Мін.', callback_data="bet_min"),
            InlineKeyboardButton(text='Подвоїти', callback_data="bet_x2"),
            InlineKeyboardButton(text='Макс.', callback_data="bet_max")
        ],
        *btns_after_bet,
        [
            InlineKeyboardButton(text='Назад', callback_data="all_games"),
            InlineKeyboardButton(text=play_text, callback_data="game_play")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def _btn_replenish():
    return [InlineKeyboardButton(text='Віддай гроші', callback_data="end_money")]
