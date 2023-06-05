from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.states import Menu, StateKeys
from bot.menus.admin_menus.admin_menu import admin_menu
from bot.menus.admin_menus.spam_confirm_menu import approve_spam_msg
from bot.menus.admin_menus.spam_language_menu import spam_language_menu
from bot.menus.admin_menus.spam_type_menu import spam_type_menu
from bot.utils.config_reader import config

router = Router()


@router.message(F.chat.type == "private", Command("admin"))
async def hi_admin(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_admin = str(user_id) in config.admin_ids

    if is_admin:
        text, kb = admin_menu()
        msg = await state.bot.send_message(message.from_user.id, text, reply_markup=kb)
        await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})


@router.callback_query(Text("admin_menu"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    text, kb = admin_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)
