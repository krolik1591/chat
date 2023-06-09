from pprint import pprint

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.consts.const import WOF_MAX_NUM
from bot.db import db
from bot.menus.main_menus.wheel_of_fortune_menus import check_status_menu, wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_wheel_info()
    user_wof_win = await db.get_user_wof_win(call.from_user.id)

    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(user_wof_win)
        await call.message.edit_text(text, reply_markup=keyboard)
        return

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, wof_info.timestamp_end, user_tickets, user_wof_win)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("my_numbers"))
async def my_numbers(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_wheel_info()

    user_selected_tickets = await db.get_number_of_user_tickets(call.from_user.id, 'selected')
    user_random_tickets = await db.get_number_of_user_tickets(call.from_user.id, 'random')

    selected_tickets = format_numbers(user_selected_tickets)[0]
    random_tickets = format_numbers(user_random_tickets)[1]

    text, kb = check_status_menu(selected_tickets, random_tickets)
    await call.message.edit_text(text, reply_markup=kb)


def format_numbers(numbers):
    formatted_rows = []
    max_digits = len(str(max(numbers)))  # Визначаємо максимальну кількість цифр у числах
    row = []
    block = []
    for i, num in enumerate(numbers, 1):
        row.append(f"<code>{str(num).zfill(max_digits)}</code>")
        if i % 3 == 0:
            block.append(" | ".join(row))
            row = []
            if len(block) == 20:
                formatted_rows.append("\n".join(block))
                block = []
    if row:
        block.append(" | ".join(row))
    if block:
        formatted_rows.append("\n".join(block))
    return formatted_rows

# def format_numbers(numbers):
#     formatted_text = ""
#     max_digits = len(str(max(numbers)))  # Визначаємо максимальну кількість цифр у числах
#     for i in range(0, len(numbers), 3):
#         row = [f"<code>{str(num).zfill(max_digits)}</code>" for num in numbers[i:i+3]]
#         formatted_text += " | ".join(row) + "\n"
#     return formatted_text

if __name__ == '__main__':
    print(format_numbers([1416517, 2156777, 7443131, 7781460, 6184808, 1839152, 795318, 5099228, 7820959, 2495254, 362147, 8057610, 9407684, 820360, 7793371, 4868105, 205015, 8285130, 5555, 7035628, 2425556, 6590537, 7967551, 6561894, 1008904, 114702, 3686845, 2215093, 6504047, 4551579, 9849436, 4849080, 5373049, 4528044, 4451013, 1742155, 3144434, 3532678, 123, 6067845, 7283049, 4699202, 5893885, 475249, 1480030, 265927, 9679949, 2932496, 232, 5808303, 9122605, 2195558, 4567497, 3620381, 7596391, 9798588, 1889695, 8753279, 6712111]))