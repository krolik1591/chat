import random

from aiogram import F, Router, types
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from bot.db import methods as db
from bot.utils.config_reader import config

router = Router()


@router.message(F.chat.type.in_(['group', 'supergroup']))
async def on_user_join(message: types.Message, state: FSMContext):
    print('on user join')
    try:
        new_chat_member_id = message.new_chat_members[0].id
    except TypeError:
        raise SkipHandler

    bot_id = state.bot.id
    if new_chat_member_id == bot_id:
        inviter_user_id = message.from_user.id
        admins = config.admin_ids
        if str(inviter_user_id) not in admins:
            await message.answer("Тільки адмін може додавати бота в чат!")
            await state.bot.leave_chat(message.chat.id)
            return
    raise SkipHandler


@router.message(Command("casino"))
async def casino(message: types.Message):
    if not await db.is_user_exists(message.from_user.id):
        await db.add_new_user(message.from_user.id, message.from_user.username)


@router.message((F.chat.type.in_(['group', 'supergroup'])) and
                (lambda message: message.dice.emoji in ['🎲', '🎯', '🏀', '⚽️', '🎰', '🎳', '🎯']))
async def play(message: types.Message):
    print('play')
    try:
        dice_value = message.dice.value
        emoji = message.dice.emoji
    except AttributeError:
        return

    if not await db.is_user_exists(message.from_user.id):
        await db.add_new_user(message.from_user.id, message.from_user.username)

    await db.add_game_result(message.from_user.id, emoji, dice_value)