from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import MENU_TEXT


def game_choice_menu(main_balance, demo_balance):
    text = MENU_TEXT.format(main_balance=main_balance, demo_balance=demo_balance)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Слоти', callback_data="casino"),
            InlineKeyboardButton(text='Кубік', callback_data="random_cube")
        ],
        [
            InlineKeyboardButton(text='Баскет', callback_data="basket"),
            InlineKeyboardButton(text='Дартс', callback_data="darts")
        ],
        [
            InlineKeyboardButton(text='Боулінг', callback_data="bowling"),
            InlineKeyboardButton(text='Футбол', callback_data="football")
        ],
        [
            InlineKeyboardButton(text='Міни', callback_data="mine"),
            InlineKeyboardButton(text='Цу-Е-Фа', callback_data="cuefa")
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)