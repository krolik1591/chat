from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import MIN_BET
from bot.texts import DEFAULT_BALANCE_TEXT, DEFAULT_PLAY_TEXT, DEMO_FUNDS_ICON


def game_menu_base(
        balance, bet, token_id,
        text=DEFAULT_BALANCE_TEXT,
        token_icon=DEMO_FUNDS_ICON,
        play_text=DEFAULT_PLAY_TEXT,
        back_to='tokens'
):
    text = text.format(balance=balance, bet=bet)

    add_replenish_btn = token_id == 1 and balance < MIN_BET
    kb = _keyboard(bet, token_icon, play_text, add_replenish_btn, back_to)

    return text, kb


def _keyboard(bet, token_icon, play_text, add_replenish_btn, back_to):
    kb = [

        *(_btn_replenish() if add_replenish_btn else []),
        [
            InlineKeyboardButton(text='-', callback_data="bet_minus"),
            InlineKeyboardButton(text=f'{bet}{token_icon}', callback_data="bet_token_icon"),
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
