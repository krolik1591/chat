from math import ceil

from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import display_ticket_num_text_menu, my_numbers_menu, \
    wheel_of_fortune_doesnt_exist_menu

router = Router()

# todo throttling


TICKETS_ON_PAGE = 3 * 20


@router.callback_query(Text("my_numbers"))
async def my_numbers(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.delete_message)
    await state.update_data({StateKeys.PREVIOUS_BALANCE_TYPE: 'general'})

    selected_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'selected')
    random_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'random')

    promo_name = (await state.get_data()).get(StateKeys.ACTIVE_PROMO_NAME)
    promo_selected_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'selected', promo_name)
    promo_random_tickets_count = await db.get_count_user_tickets(call.from_user.id, 'random', promo_name)

    if not await db.get_active_wheel_info():
        wof_reward = await db.get_user_wof_win(call.from_user.id)
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(wof_reward)
        await call.message.edit_text(text, reply_markup=keyboard)
        return

    if not selected_tickets_count and not random_tickets_count:
        await call.answer(_("WOF_MY_NUMBERS_MENU_NO_TICKETS"))
        return

    text, kb = my_numbers_menu(selected_tickets_count, random_tickets_count,
                               promo_selected_tickets_count, promo_random_tickets_count)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith="display_tickets_"))
async def display_user_tickets(call: types.CallbackQuery, state: FSMContext):
    ticket_type = call.data.removeprefix("display_tickets_")
    text, kb = await display_general_tickets(state, call.from_user.id, ticket_type)

    # if all_general_tickets_count == 0:
    #     await call.answer(_("WOF_MY_NUMBERS_MENU_NO_TICKETS"))
    #     return

    await call.message.edit_text(text, reply_markup=kb)
    await state.set_state(Menu.enter_pages)


@router.callback_query(Text(startswith="change_tickets_type_balance"))
async def display_another_tickets(call: types.CallbackQuery, state: FSMContext):
    previous_balance_type = (await state.get_data()).get(StateKeys.PREVIOUS_BALANCE_TYPE)

    if previous_balance_type == 'general':
        await state.update_data({StateKeys.PREVIOUS_BALANCE_TYPE: 'promo'})
        ticket_type = (await state.get_data()).get(StateKeys.TICKET_TYPE)
        promo_name = (await state.get_data()).get(StateKeys.ACTIVE_PROMO_NAME)

        text, kb = await display_general_tickets(state, call.from_user.id, ticket_type, promo_name)

    else:   # previous_balance_type == 'promo'
        await state.update_data({StateKeys.PREVIOUS_BALANCE_TYPE: 'general'})
        ticket_type = (await state.get_data()).get(StateKeys.TICKET_TYPE)

        text, kb = await display_general_tickets(state, call.from_user.id, ticket_type)

    await call.message.edit_text(text, reply_markup=kb)
    await state.set_state(Menu.enter_pages)


async def display_general_tickets(state, user_id, ticket_type, promo_name=None):
    tickets_count = await db.get_count_user_tickets(user_id, ticket_type, promo_name)

    total_pages = ceil(tickets_count / TICKETS_ON_PAGE)
    await state.update_data(**{StateKeys.CURRENT_PAGE: 1,
                               StateKeys.TOTAL_PAGES: total_pages,
                               StateKeys.TICKET_TYPE: ticket_type,
                               })

    tickets_text = await get_tickets_on_page(user_id, ticket_type, 1, promo_name)
    text, kb = display_ticket_num_text_menu(tickets_text, 1, total_pages)
    return text, kb


@router.callback_query(Text(startswith="ticket_page_"))
async def scroll_ticket_pages(call: types.CallbackQuery, state: FSMContext):
    scroll = call.data.removeprefix("ticket_page_")
    data = await state.get_data()

    new_page = data[StateKeys.CURRENT_PAGE] + (1 if scroll == "next" else -1)
    if new_page < 1 or new_page > data[StateKeys.TOTAL_PAGES]:
        await call.answer()
        return

    await state.update_data(**{StateKeys.CURRENT_PAGE: new_page})
    if data[StateKeys.PREVIOUS_BALANCE_TYPE] == 'promo':
        promo_name = data[StateKeys.ACTIVE_PROMO_NAME]
        tickets_text = await get_tickets_on_page(call.from_user.id, data[StateKeys.TICKET_TYPE], new_page, promo_name)
    else:
        tickets_text = await get_tickets_on_page(call.from_user.id, data[StateKeys.TICKET_TYPE], new_page)

    text, kb = display_ticket_num_text_menu(tickets_text, new_page, data[StateKeys.TOTAL_PAGES])
    await call.message.edit_text(text, reply_markup=kb)


@router.message(StateFilter(Menu.enter_pages))
async def enter_pages(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()

    try:
        new_page = int(message.text)
    except ValueError:
        return

    if new_page < 1 or new_page > data[StateKeys.TOTAL_PAGES]:
        return

    await state.update_data(**{StateKeys.CURRENT_PAGE: new_page})
    tickets_text = await get_tickets_on_page(message.from_user.id, data[StateKeys.TICKET_TYPE], new_page)

    text, kb = display_ticket_num_text_menu(tickets_text, new_page, data[StateKeys.TOTAL_PAGES])
    await state.bot.edit_message_text(text, message.from_user.id, data[StateKeys.LAST_MSG_ID], reply_markup=kb)


async def get_tickets_on_page(user_id, ticket_type, page, promo_name=None):
    page_tickets = await db.get_user_ticket_numbers(user_id, ticket_type, offset=TICKETS_ON_PAGE * (page - 1), limit=TICKETS_ON_PAGE, promo_name=promo_name)
    tickets_text = get_display_tickets_num_text(page_tickets)
    return tickets_text


def get_display_tickets_num_text(tickets_num):
    items_in_row = 3
    tickets_rows = [tickets_num[i:i + items_in_row]
                    for i in range(0, len(tickets_num), items_in_row)]

    return "\n".join(
        ' | '.join([f"<code>{num:07d}</code>" for num in row])
        for row in tickets_rows
    )
