from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import texts
from bot.menus.utils import get_balance_icon


def cube_settings(selected_setting, balance, bet, balance_type):
    balance_icon = get_balance_icon(balance_type)
    general_bet = len(selected_setting) * bet
    text = texts.CUBE_SETTINGS_TEXT.format(balance=balance, token_icon=balance_icon, general_bet=general_bet)
    bet_text = texts.CUBE_BET_BUTTON.format(bet=bet, token_icon=balance_icon)
    kb = _keyboard(bet_text, selected_setting, play_text=texts.CUBE_PLAY_TEXT)

    return text, kb


CUBE_VARIANTS = [
    ['1', '2', '3', '4', '5', '6'],
    ['12', '34', '56'],
    ['246', '135']
]


def _keyboard(bet_text, selected_setting, play_text):
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
        '246': texts.CUBE_SETTINGS_BTN_EVEN,
        '135': texts.CUBE_SETTINGS_BTN_ODD,
    }

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
         InlineKeyboardButton(text=texts.CUBE_SETTINGS_BTN_RESET_ALL_BETS, callback_data="cube_game_settings_RESET")],
        *settings_btns,
        [
            InlineKeyboardButton(text=texts.BTN_BACK, callback_data="select_balance_type"),
            InlineKeyboardButton(text=play_text, callback_data="game_play")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
