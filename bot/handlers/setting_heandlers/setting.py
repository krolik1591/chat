from aiogram import Router, types
from aiogram.dispatcher.filters import Text

from bot.db.methods import set_user_lang
from bot.menus.setting_menus.language_menu import language_menu
from bot.menus.setting_menus.setting import setting_menu

router = Router()


@router.callback_query(text=["settings"])
async def settings(call: types.CallbackQuery):
    text, keyboard = setting_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["change_lang"])
async def change_lang(call: types.CallbackQuery):
    text, keyboard = language_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(text_startswith='new_lang'))
async def update_language(call: types.CallbackQuery):
    lang = call.data.removeprefix('new_lang')
    await set_user_lang(call.from_user.id, lang)

    await call.answer('Мову змінено!')