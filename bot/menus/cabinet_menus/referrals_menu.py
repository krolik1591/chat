from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.consts.const import USER_REF_LEVEL


def referrals_menu(invite_link, referrals_count, total_ref_withdraw, referrals_bets, all_profit):

    NAME_REF_LEVELS = {
        'adept': _('REF_LVL_1_ADEPT'),
        'experienced': _('REF_LVL_2_EXPERIENCED'),
        'connoisseur': _('REF_LVL_3_CONNOISSEUR'),
        'expert': _('REF_LVL_4_EXPERT'),
        'maestro': _('REF_LVL_5_MAESTRO')
    }

    reverse_ref_lvl = reversed(list(USER_REF_LEVEL.items()))

    for name, (profit, percent) in reverse_ref_lvl:
        if profit <= all_profit:
            ref_level_name = NAME_REF_LEVELS[name]
            ref_level_percent = percent
            break
    else:
        raise Exception('ref_level not found')

    text = _('REFERRAL_MENU_TEXT').format(invite_link=invite_link, referrals_count=referrals_count,
                                          total_ref_withdraw=total_ref_withdraw, referrals_bets=referrals_bets,
                                          all_profit=all_profit, ref_level_name=ref_level_name,
                                          ref_level_percent=ref_level_percent)
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
            InlineKeyboardButton(text=_('BTN_BACK'), callback_data="my_account")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
