from aiogram import Router, types
from aiogram.filters import Text

from bot.menus.main_menus.guides_menus import guides_menu

router = Router()


@router.callback_query(Text("guides"))
async def settings(call: types.CallbackQuery):

    text, keyboard = guides_menu()
    await call.message.edit_text(text, reply_markup=keyboard)
