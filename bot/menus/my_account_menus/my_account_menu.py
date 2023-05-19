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
            InlineKeyboardButton(text=_('CABINET_MENU_BTN_REFERRALS'), callback_data="referrals_menu")
        ],
        [
            InlineKeyboardButton(text='Промокоди', callback_data="promo_codes")
        ],
        [
            InlineKeyboardButton(text='Трофеї', callback_data="trophies"),
        ],
        [
            InlineKeyboardButton(text='Відправити подарунок', callback_data="send_gift"),
            InlineKeyboardButton(text='Налаштування', callback_data="settings"),

        ],
        [
            InlineKeyboardButton(text='Меню', callback_data="main_menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
