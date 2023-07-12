from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.menus.utils import balances_text
from aiogram.utils.i18n import gettext as _


def my_account_menu(balances: dict):
    text = _('MENU_TEXT').format(balances=balances_text(balances))
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('ACCOUNT_MENU_BTN_REFERRALS'), callback_data="referrals_menu_start")
        ],
        [
            InlineKeyboardButton(text=_('ACCOUNT_MENU_BTN_PROMO_CODES'), callback_data="promo_codes")
        ],
        [
            InlineKeyboardButton(text=_('ACCOUNT_MENU_BTN_TROPHIES'), callback_data="trophies"),
        ],
        [
            InlineKeyboardButton(text=_('ACCOUNT_MENU_BTN_SEND_GIFT'), callback_data="send_gift"),
            InlineKeyboardButton(text=_('ACCOUNT_MENU_SETTINGS'), callback_data="settings"),
        ],
        [
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="main_menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def promo_code_menu():
    text = _('ACCOUNT_MENU_PROMO_CODES_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("ACCOUNT_MENU_ACTIVE_PROMO_CODES_BTN"), callback_data="active_promo_codes")],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="my_account")]
    ])

    return text, kb


def active_promo_code_menu(text):
    text = _('ACCOUNT_MENU_ACTIVE_PROMO_CODES_TEXT').format(text=text)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="my_account")]
    ])

    return text, kb
