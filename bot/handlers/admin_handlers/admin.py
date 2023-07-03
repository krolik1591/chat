import base64
import hashlib
import hmac
import json
import time

from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.states import StateKeys
from bot.menus.admin_menus.admin_menu import admin_menu
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


@router.message(F.chat.type == "private", Command("admin_login"))
async def admin_login(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_admin = str(user_id) in config.admin_ids

    if not is_admin:
        return

    auth = {
        "auth_date": time.time(),
        "first_name": message.from_user.first_name,
        "id": message.from_user.id,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username
    }
    auth = {k: v for k, v in auth.items() if v is not None}

    bot_token = state.bot.token.encode()
    bot_token = hashlib.sha256(bot_token).digest()
    token = "\n".join(sorted([f"{k}={v}" for k, v in auth.items() if k != "hash"]))
    token_hash = hmac.new(bot_token, token.encode(), hashlib.sha256).hexdigest()
    auth["hash"] = token_hash

    encoded_bytes = base64.b64encode(json.dumps(auth).encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    await message.answer(f'<code>{encoded_string}</code>')
