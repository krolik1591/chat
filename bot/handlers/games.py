import random
from pprint import pprint

from aiogram import F, Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, Text
from aiogram.types import ChatMemberUpdated

from bot.db.methods import add_game_result, add_new_promo_to_user, add_new_user, get_all_promos, get_user_promos, \
    is_user_exists

router = Router()


@router.message(F.chat.type.in_(['group', 'supergroup']))
async def on_user_join(message: types.Message):
    x = message.new_chat_members
    inviter_user_id = message.from_user.id
    pprint(x[0].__dict__)
    print(inviter_user_id)


@router.message(Text(startswith="/casino"))
async def casino(message: types.Message):
    if not await is_user_exists(message.from_user.id):
        await add_new_user(message.from_user.id, message.from_user.username)

    user_num = message.text.removeprefix("/casino")
    try:
        user_num = int(user_num)
    except ValueError:
        await message.answer("Ви маєте ввести /casino 'number' (де number - ціле число)")
        return

    random_num = random.randint(0, 100)
    if user_num != random_num:
        await message.answer(f"Ви програли, число було {random_num}")
        return

    exist_promos = await get_all_promos()
    active_user_promos = await get_user_promos(message.from_user.id)
    available_promo = list(set(exist_promos).difference(active_user_promos))
    if not available_promo:
        await message.answer("Ви виграли, але всі промокоди вже використані!")
        return

    await add_new_promo_to_user(message.from_user.id, available_promo[0])
    await message.answer(f"Ви отримали промокод {available_promo[0]}")


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
