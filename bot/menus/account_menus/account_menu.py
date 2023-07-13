from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.menus.utils import balances_text


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
