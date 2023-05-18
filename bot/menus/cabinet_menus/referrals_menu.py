from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.i18n import gettext as _


def referrals_menu(invite_link, referrals_count, total_ref_withdraw):
    text = _('REFERRAL_MENU_TEXT').format(invite_link=invite_link, referrals_count=referrals_count,
                                          total_ref_withdraw=total_ref_withdraw)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text=_('REFERRALS_MENU_SEND_INVITE'), switch_inline_query="send_invite"),
        ],
        [
            InlineKeyboardButton(text=_('REFERRALS_MENU_SEND_PROMO_TO_GENERAL'), callback_data="promo_to_general")
        ],
        [
            InlineKeyboardButton(text=_('REFERRALS_MENU_HOW_IT_WORKS'), callback_data="ref_info")
        ],
        [
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="cabinet_menu")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
