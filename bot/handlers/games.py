import json
from pprint import pprint

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db.users import add_game_result, add_new_user, is_user_exists

router = Router()


@router.message()
async def play(message: types.Message):
    try:
        dice_value = message.dice.value
        emoji = message.dice.emoji
    except AttributeError:
        return

    if not await is_user_exists(message.from_user.id):
        await add_new_user(message.from_user.id, message.from_user.username)

    await add_game_result(message.from_user.id, emoji, dice_value)
