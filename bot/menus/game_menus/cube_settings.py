from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.menus.utils import get_balance_icon
from bot.texts import CUBE_BET_BUTTON, CUBE_PLAY_TEXT, CUBE_SETTINGS_TEXT


def cube_settings(selected_setting, balance, bet, balance_type):
    balance_icon = get_balance_icon(balance_type)
    general_bet = len(selected_setting) * bet
    text = CUBE_SETTINGS_TEXT.format(balance=balance, token_icon=balance_icon, general_bet=general_bet)
    bet_text = CUBE_BET_BUTTON.format(bet=bet, token_icon=balance_icon)
    kb = _keyboard(bet_text, selected_setting, play_text=CUBE_PLAY_TEXT)

    return text, kb


CUBE_VARIANTS = [
    ['1', '2', '3', '4', '5', '6'],
    ['12', '34', '56'],
    ['246', '135']
]

# todo i18n
CUBE_NAMES = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '12': '1-2',
    '34': '3-4',
    '56': '5-6',
    '246': 'Парне',
    '135': 'Непарне',
}


def _keyboard(bet_text, selected_setting, play_text):
    def btn_text(key_name):
        name = CUBE_NAMES[key_name]
        if key_name in selected_setting:
            return '•' + name + '•'
        return name

    settings_btns = [[
        InlineKeyboardButton(text=btn_text(key_name), callback_data="cube_game_settings_" + key_name)
        for key_name in row
    ] for row in CUBE_VARIANTS]

    kb = [
        [InlineKeyboardButton(text=bet_text, callback_data="bet"),
         InlineKeyboardButton(text='Ставка', callback_data="reset_bet")],
        *settings_btns,
        [
            InlineKeyboardButton(text='Назад', callback_data="select_balance_type"),
            InlineKeyboardButton(text=play_text, callback_data="game_play")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
