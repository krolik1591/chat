from random import randint

from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext

from bot.consts.const import DEFAULT_TICKET_COUNT, WOF_MAX_NUM, WOF_MIN_NUM
from bot.db import db, manager
from bot.handlers.states import Menu, StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import buy_random_num_menu, buy_selected_num_menu, buy_ticket_menu
from bot.menus.utils import kb_del_msg

from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(Text("buy_ticket"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.delete_message)
    wof_info, user_balance, user_tickets = await display_wof_info(call.from_user.id)

    text, keyboard = buy_ticket_menu(wof_info, user_balance, user_tickets)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_selected_num"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.enter_ticket_num)
    wof_info, user_balance, user_tickets = await display_wof_info(call.from_user.id)

    text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.enter_ticket_num))
async def enter_ticket_num(message: types.Message, state: FSMContext):
    await message.delete()

    ticket_num = message.text
    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    wof_info, user_balance, user_tickets = await display_wof_info(message.from_user.id)

    if await check_ticket_num(message, ticket_num):
        return

    text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets, ticket_num)
    try:
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)
    except exceptions.TelegramBadRequest as e:
        print("User enter the same ticket num")

    await state.update_data(**{StateKeys.TICKET_NUM: ticket_num})


@router.callback_query(Text("buy_random_num"))
async def buy_random_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.enter_tickets_count)

    wof_info, user_balance, user_tickets = await display_wof_info(call.from_user.id)
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost

    if how_much_tickets_can_buy <= DEFAULT_TICKET_COUNT:
        await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: how_much_tickets_can_buy})
    else:
        await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: DEFAULT_TICKET_COUNT})
        how_much_tickets_can_buy = DEFAULT_TICKET_COUNT

    text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, how_much_tickets_can_buy)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(startswith="change_tickets_count_"))
async def update_ticket_count_btn(call: types.CallbackQuery, state: FSMContext):
    wof_info, user_balance, user_tickets = await display_wof_info(call.from_user.id)
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost

    count_update = call.data.removeprefix("change_tickets_count_")
    tickets_count = (await state.get_data()).get(StateKeys.RANDOM_TICKETS_COUNT)

    if count_update == '+':
        if tickets_count >= how_much_tickets_can_buy:
            await call.answer(_('WOF_BUY_TICKET_ERR_CHOOSE_SMALLER_QUANTITY')
                              .format(how_much_tickets_can_buy=how_much_tickets_can_buy),
                              show_alert=True)
            return
        await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: tickets_count + 1})
    else:
        if tickets_count <= 1:
            await call.answer(_('WOF_BUY_TICKET_ERR_MIN_TICKETS_COUNT'), show_alert=True)
            return
        await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: tickets_count - 1})

    tickets_count = (await state.get_data()).get(StateKeys.RANDOM_TICKETS_COUNT)
    text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, tickets_count)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.enter_tickets_count))
async def enter_tickets_count(message: types.Message, state: FSMContext):
    await message.delete()

    wof_info, user_balance, user_tickets = await display_wof_info(message.from_user.id)
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost
    tickets_count = message.text

    if await check_ticket_count(message, tickets_count, how_much_tickets_can_buy):
        return

    await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: tickets_count})

    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, tickets_count)
    await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)


@router.callback_query(Text(startswith="buy_ticket_"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):
    buy_ticket_type = call.data.removeprefix("buy_ticket_")
    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    wof_info = await db.get_wheel_info()

    if buy_ticket_type == 'selected_num':
        ticket_num = (await state.get_data()).get(StateKeys.TICKET_NUM)
        ticket_type = 'selected'

        if await db.check_ticket_in_db(ticket_num):
            await call.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), show_alert=True)
            return
        tickets = [ticket_num]

    else:
        tickets_count = (await state.get_data()).get(StateKeys.RANDOM_TICKETS_COUNT)
        ticket_type = 'random'
        tickets = await create_random_tickets(tickets_count)

    if user_balance < wof_info.ticket_cost * len(tickets):
        await call.answer(_('WOF_BUY_TICKET_ERR_NOT_ENOUGH_MONEY'), show_alert=True)
        return

    with manager.pw_database.atomic():
        for ticket in tickets:
            await db.add_new_ticket(call.from_user.id, ticket, ticket_type)
        await db.update_user_balance(call.from_user.id, 'general', -wof_info.ticket_cost * len(tickets))

    await call.answer(_('WOF_BUY_TICKET_SUCCESS'), show_alert=True)

    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    user_tickets = await db.get_user_tickets(call.from_user.id)

    if buy_ticket_type == 'selected_num':
        text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets)
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, tickets_count)
        await call.message.edit_text(text, reply_markup=keyboard)


async def create_random_tickets(tickets_count):
    result = []
    for item in range(int(tickets_count)):
        ticket_num = randint(WOF_MIN_NUM, WOF_MAX_NUM)
        while await db.check_ticket_in_db(ticket_num):
            ticket_num = randint(WOF_MIN_NUM, WOF_MAX_NUM)
        result.append(ticket_num)
    return result


async def check_ticket_num(message, ticket_num):
    if not ticket_num.isdigit():
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_NUMBERS'), reply_markup=kb_del_msg())
        return True

    if len(ticket_num) != 7:
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_7_SYMBOL'), reply_markup=kb_del_msg())
        return True

    if await db.check_ticket_in_db(ticket_num):
        await message.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), reply_markup=kb_del_msg())
        return True

    return False


async def check_ticket_count(message, tickets_count, how_much_tickets_can_buy):
    try:
        tickets_count = int(tickets_count)
    except ValueError:
        return True

    if tickets_count <= 0:
        return True

    return False


async def display_wof_info(user_id):
    wof_info = await db.get_wheel_info()
    user_balance = await db.get_user_balance(user_id, 'general')
    user_tickets = await db.get_user_tickets(user_id)
    return wof_info, user_balance, user_tickets
