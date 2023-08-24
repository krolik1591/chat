import json
from collections import Counter

from aiogram import F, Router, types
from aiogram.filters import Command, Text

from bot.db.methods import create_new_promo, get_user_promos, is_promo_in_db
from bot.utils.config_reader import config

router = Router()


@router.message(Command("add_promo"))
async def add_promo(message: types.Message):
    admins = config.admin_ids
    if str(message.from_user.id) not in admins:
        return

    promos_info = message.text.removeprefix('/add_promo').split(',')
    if not promos_info:
        await message.answer("Введіть промо!")
        return

    for promo in promos_info:
        promo_info = promo.lstrip().split(' ')
        promo_name = promo_info[0]
        try:
            number_of_uses = int(promo_info[1])
        except IndexError:
            await message.answer("Формат введення: \n/add_promo promo_name1 number_of_uses1, promo_name2 number_of_uses2, ...")
            return
        except ValueError:
            await message.answer("К-сть використань має бути цілим числом!")
            return

        if await is_promo_in_db(promo_name):
            await message.answer(f'Промо з назвою {promo_name} вже існує!')
            continue

        await create_new_promo(promo_name, number_of_uses)
        await message.answer(f'Промокод <code>{promo_name}</code> створено! К-сть використань: {number_of_uses}')


@router.message(F.chat.type == "private", Command("my_promos"))
async def my_promos(message: types.Message):
    active_promos = json.loads(await get_user_promos(message.from_user.id))
    if not active_promos:
        await message.answer('У вас немає промокодів!')
        return

    count_promos = Counter(active_promos)

    text = '\n'.join([f'{promo_name}: {promo_count}' for promo_name, promo_count in count_promos.items()])
    await message.answer(f'Ваші промокоди:\n\n{text}')
