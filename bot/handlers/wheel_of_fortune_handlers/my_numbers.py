from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import display_ticket_num_text, my_numbers_menu

router = Router()


@router.callback_query(Text("my_numbers"))
async def my_numbers(call: types.CallbackQuery, state: FSMContext):
    all_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    if all_tickets == 0:
        await call.answer(_("WOF_MY_NUMBERS_MENU_NO_TICKETS"))
        return

    selected_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'selected')
    random_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'random')

    text, kb = my_numbers_menu(selected_tickets_count, random_tickets_count)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith="display_tickets_"))
async def my_numbers(call: types.CallbackQuery, state: FSMContext):
    what_ticket_display = call.data.removeprefix("display_tickets_")
    if what_ticket_display == 'selected':
        user_selected_tickets = await db.get_number_of_user_tickets(call.from_user.id, 'selected')
        tickets_text = get_display_tickets_num_text(user_selected_tickets)
    else:
        user_random_tickets = await db.get_number_of_user_tickets(call.from_user.id, 'random')
        tickets_text = get_display_tickets_num_text(user_random_tickets)

    await state.update_data(**{StateKeys.TICKETS_TO_DISPLAY: tickets_text})
    await state.update_data(**{StateKeys.CURRENT_PAGE: 1})

    text, kb = display_ticket_num_text(tickets_text[0], 1, len(tickets_text))
    await call.message.edit_text(text, reply_markup=kb)
    await state.set_state(Menu.enter_pages)


@router.callback_query(Text(startswith="ticket_page_"))
async def scroll_ticket_pages(call: types.CallbackQuery, state: FSMContext):
    scroll = call.data.removeprefix("ticket_page_")
    tickets_text = (await state.get_data()).get(StateKeys.TICKETS_TO_DISPLAY)
    page = (await state.get_data()).get(StateKeys.CURRENT_PAGE)
    if scroll == 'next':
        if page + 1 > len(tickets_text):
            await call.answer()
            return
        text, kb = display_ticket_num_text(tickets_text[page + 1], page + 1, len(tickets_text))
        await call.message.edit_text(text, reply_markup=kb)
        await state.update_data(**{StateKeys.CURRENT_PAGE: page + 1})

    else:
        if page == 1:
            await call.answer()
            return
        text, kb = display_ticket_num_text(tickets_text[page - 1], page - 1, len(tickets_text))
        await call.message.edit_text(text, reply_markup=kb)
        await state.update_data(**{StateKeys.CURRENT_PAGE: page - 1})


@router.message(StateFilter(Menu.enter_pages))
async def enter_pages(message: types.Message, state: FSMContext):
    await message.delete()

    tickets_text = (await state.get_data()).get(StateKeys.TICKETS_TO_DISPLAY)
    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    page = message.text
    try:
        page = int(page)
    except ValueError:
        return

    if page > len(tickets_text) or page < 1:
        return

    text, kb = display_ticket_num_text(tickets_text[page], page, len(tickets_text))
    await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=kb)
    await state.update_data(**{StateKeys.CURRENT_PAGE: page})


def get_display_tickets_num_text(tickets_num):
    formatted_rows = []
    max_digits = len(str(max(tickets_num)))
    row = []
    block = []
    for i, num in enumerate(tickets_num, 1):
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
