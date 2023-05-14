from aiogram import Router, types
from aiogram.filters import Text, Command, StateFilter
from aiogram.utils.deep_linking import create_start_link

from bot.handlers.states import Menu
from bot.utils.config_reader import config

router = Router()


@router.callback_query(Text("delete_message"))
async def delete_message(call: types.CallbackQuery):
    await call.message.delete()


@router.message(Command("admin"))
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    is_admin = str(user_id) in config.admin_ids


@router.message(StateFilter(Menu.delete_message))
async def delete_message(message: types.Message):
    await message.delete()

