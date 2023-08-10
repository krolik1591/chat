from aiogram import F, Router, types
from aiogram.filters import Command, Text

from bot.utils.config_reader import config

router = Router()


@router.message(Text("/add_promo"))
async def add_promo(message: types.Message):
    print('hi bitch')
    admins = config.admin_ids
    if str(message.from_user.id) not in admins:
        return

