from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_del_msg():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='OK', callback_data="delete_message")
    ]])
