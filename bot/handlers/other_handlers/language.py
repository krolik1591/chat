from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.db.methods import set_user_lang
from bot.handlers.context import Context
from bot.handlers.m01_main import send_main_menu
from bot.menus.main_menus.language_menu import language_menu

router = Router()


@router.callback_query(Text("change_lang"))
async def change_lang(call: types.CallbackQuery):
    text, keyboard = language_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(startswith='new_lang'))
async def update_language(call: types.CallbackQuery, state: FSMContext, i18n_middleware):
    user_lang = call.data.removeprefix('new_lang')
    await set_user_lang(call.from_user.id, user_lang)
    await i18n_middleware.set_locale(state, user_lang)

    await call.answer(_('SETTINGS_LANG_CHANGED'))

    last_msg_id = (await state.get_data()).get('last_msg_id')
    context = await Context.from_fsm_context(call.from_user.id, state)
    await send_main_menu(context, last_msg_id)
