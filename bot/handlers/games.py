import json
from pprint import pprint

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def play(message: types.Message):
    try:
        emoji = json.loads(message.json())['dice']['emoji']
        dice_value = json.loads(message.json())['dice']['value']
    except TypeError:
        return

    print(emoji, dice_value)

