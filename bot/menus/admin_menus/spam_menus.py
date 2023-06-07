from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.menus.main_menus.language_menu import LANGUAGES


def spam_type_menu():
    text = _('ADMIN_SPAM_TYPE_MENU_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("ADMIN_SPAM_TYPE_MENU_BTN_ALL_USERS"), callback_data="who_get_spam_all"), ],
        [InlineKeyboardButton(text=_("ADMIN_SPAM_TYPE_MENU_BTN_FOR_ID"), callback_data="who_get_spam_for_id"), ],
        [InlineKeyboardButton(text=_("BTN_BACK"), callback_data="admin_menu"), ]
    ])

    return text, kb


def approve_spam_msg():
    text = _('ADMIN_SPAM_CONFIRM_MENU_TEXT')
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("ADMIN_SPAM_CONFIRM_MENU_BTN_APPROVE"), callback_data="spam_sending_approved"),
            InlineKeyboardButton(text=_("ADMIN_SPAM_CONFIRM_MENU_BTN_DENIED"), callback_data="spam_sending_")
        ]
    ])

    return text, kb


def spam_language_menu():
    text = _('ADMIN_SPAM_LANGUAGE_MENU_TEXT')
    kb = _keyboard()

    return text, kb


def _keyboard():
    settings_btns = [
        [InlineKeyboardButton(text=LANGUAGES[lang], callback_data="spam_lang" + lang)]
        for lang in LANGUAGES
    ]

    kb = [
        *settings_btns,
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="spam_type")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def incorrect_user_menu(not_exist_text, another_lang_text, spam_lang):
    text = _("ADMIN_SPAM_TEXT_WHICH_USER_DOESNT_EXIST").format(not_exist_receiver=not_exist_text,
                                                               another_lang=another_lang_text)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('ADMIN_SPAM_INCORRECT_USER_MENU_BTN_BACK'), callback_data="spam_lang" + spam_lang), ],
        [InlineKeyboardButton(text=_('ADMIN_SPAM_INCORRECT_USER_MENU_BTN_GO_NEXT'), callback_data="list_for_spam_approved"), ],
    ])

    return text, kb
