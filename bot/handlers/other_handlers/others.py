from aiogram import Router, types
from aiogram.filters import StateFilter, Text

from bot.handlers.states import Menu

router = Router()


@router.callback_query(Text("delete_message"))
async def delete_message(call: types.CallbackQuery):
    await call.message.delete()


@router.message(StateFilter(Menu.delete_message))
async def delete_message(message: types.Message):
    await message.delete()

