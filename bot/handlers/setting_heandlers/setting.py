from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db.methods import set_user_lang
from bot.handlers.context import Context
from bot.handlers.m01_main import send_main_menu
from bot.handlers.states import StateKeys
from bot.menus.setting_menus.language_menu import language_menu
from bot.menus.setting_menus.setting import setting_menu

from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(Text("settings"))
async def settings(call: types.CallbackQuery):
    text, keyboard = setting_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("change_lang"))
async def change_lang(call: types.CallbackQuery):
    text, keyboard = language_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(startswith='new_lang'))
async def update_language(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.removeprefix('new_lang')
    await set_user_lang(call.from_user.id, lang)
    await state.update_data(**{StateKeys.LOCALE: lang})

    await call.answer(_('SETTINGS_LANG_CHANGED'))

    context = await Context.from_fsm_context(call.from_user.id, state)
    await send_main_menu(context)
