from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts.texts import REFERRAL_MENU_TEXT


def referrals_menu(invite_link):
    text = REFERRAL_MENU_TEXT.format(invite_link=invite_link)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Відправити запрошення', switch_inline_query="send_invite"),
        ],
        [
            InlineKeyboardButton(text='Вивести на ігровий баланс', callback_data="promo_to_general")
        ],
        [
            InlineKeyboardButton(text='Як це працює', callback_data="ref_info")
        ],
        [
            InlineKeyboardButton(text='‹ Назад', callback_data="referrals_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
