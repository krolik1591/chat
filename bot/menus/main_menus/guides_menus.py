from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.i18n import gettext as _


def guides_menu():
    text = _('GUIDES_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_ABOUT_CASINO'), callback_data="wallet_menu"),
        ],
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_HOW_TO_DEPOSIT'), callback_data="how_to_deposit")
        ],
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_WITHDRAWALS'), callback_data="withdrawals")
        ],
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_GAMES_AND_RULES'), callback_data="games_and_rules"),
        ],
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_PROMO_CODES'), callback_data="promo_codes")
        ],
        [
            InlineKeyboardButton(text=_('GUIDES_MENU_BTN_REFERRAL_PROGRAM'), callback_data="referral_program")
        ],
        [
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
