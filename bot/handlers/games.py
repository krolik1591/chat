import random

from aiogram import F, Router, types
from aiogram.filters import Text

from bot.db.methods import add_game_result, add_new_user, is_user_exists

router = Router()


@router.message(Text(startswith="/casino"))
async def casino(message: types.Message):
    user_num = message.text.removeprefix("/casino")
    try:
        user_num = int(user_num)
    except ValueError:
        await message.answer("Ви маєте ввести /casino <number>")
        return

    random_num = random.randint(0, 100)
    if user_num == random_num:
        await message.answer("Ви виграли!")
    else:
        await message.answer(f"Ви програли, число було {random_num}")


@router.message()
async def play(message: types.Message):
    print('from play')
    try:
        dice_value = message.dice.value
        emoji = message.dice.emoji
    except AttributeError:
        return

    if not await is_user_exists(message.from_user.id):
        await add_new_user(message.from_user.id, message.from_user.username)

    await add_game_result(message.from_user.id, emoji, dice_value)
