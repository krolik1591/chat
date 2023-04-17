from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import ADMIN_APPROVE_TX, SUCCESSFUL_REPLENISH_MENU


SUCCESSFUL_TEXT = {
    'successful_classic': SUCCESSFUL_REPLENISH_MENU,
    'successful_manual': ADMIN_APPROVE_TX
}


def successful_replenish_menu(text_, amount):
    text = SUCCESSFUL_TEXT[text_].format(amount=amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [

        [
            InlineKeyboardButton(text='ОК', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)