import random
import time

from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.consts.const import DEFAULT_TICKET_COUNT, MAX_BUY_TICKETS_PER_ONE_CLICK, WOF_MAX_NUM, WOF_MIN_NUM
from bot.db import db, manager
from bot.handlers.states import Menu, StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import buy_random_num_menu, buy_selected_num_menu, buy_ticket_menu
from bot.menus.utils import kb_del_msg

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
        print("User enter the same ticket num", e)

    await state.update_data(**{StateKeys.TICKET_NUM: ticket_num})


@router.callback_query(Text("buy_random_num"))
async def buy_random_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.enter_tickets_count)

    wof_info, user_balance, user_tickets = await display_wof_info(call.from_user.id)
    how_much_tickets_can_buy = int(user_balance // wof_info.ticket_cost)

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

    count_update = call.data.removeprefix("change_tickets_count_")
    data = await state.get_data()

    new_tickets_count = data[StateKeys.RANDOM_TICKETS_COUNT] + (1 if count_update == "+" else -1)
    if new_tickets_count < 1:
        await call.answer()
        return
    await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: new_tickets_count})

    text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, new_tickets_count)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.enter_tickets_count))
async def enter_tickets_count(message: types.Message, state: FSMContext):
    await message.delete()

    wof_info, user_balance, user_tickets = await display_wof_info(message.from_user.id)
    how_much_tickets_can_buy = user_balance // wof_info.ticket_cost
    tickets_count = message.text

    if await check_ticket_count(tickets_count):
        return

    await state.update_data(**{StateKeys.RANDOM_TICKETS_COUNT: int(tickets_count)})

    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, tickets_count)
    await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)


@router.callback_query(Text(startswith="buy_ticket_"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):
    buy_ticket_type = call.data.removeprefix("buy_ticket_")
    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    wof_info = await db.get_active_wheel_info()
    if not wof_info:
        await call.answer(_('WOF_BUY_TICKET_ERR_NO_ACTIVE_WHEEL'), show_alert=True)
        return

    if buy_ticket_type == 'selected_num':
        ticket_num = (await state.get_data()).get(StateKeys.TICKET_NUM)
        ticket_type = 'selected'

        if not ticket_num:
            await call.answer()
            return

        if await db.check_ticket_in_db(ticket_num):
            await call.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), show_alert=True)
            return
        tickets = [ticket_num]

    else:   # buy_ticket_type == 'random_num'
        tickets_count = (await state.get_data()).get(StateKeys.RANDOM_TICKETS_COUNT)
        ticket_type = 'random'

        if tickets_count > MAX_BUY_TICKETS_PER_ONE_CLICK:
            await call.answer(_('WOF_BUY_TICKET_ERR_TOO_MUCH_TICKETS')
                              .format(maximum_ticket=MAX_BUY_TICKETS_PER_ONE_CLICK), show_alert=True)
            return

        tickets = await create_random_tickets(tickets_count)

    if not tickets:
        await call.answer(_('WOF_BUY_TICKET_ERR_NO_TICKETS'), show_alert=True)
        return

    if user_balance < wof_info.ticket_cost * len(tickets):
        await call.answer(_('WOF_BUY_TICKET_ERR_NOT_ENOUGH_MONEY'), show_alert=True)
        return

    with manager.pw_database.atomic():
        await db.add_new_ticket(call.from_user.id, tickets, ticket_type)
        await db.update_user_balance(call.from_user.id, 'general', -wof_info.ticket_cost * len(tickets))

    await call.answer(_('WOF_BUY_TICKET_SUCCESS'), show_alert=True)

    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')

    if buy_ticket_type == 'selected_num':
        text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets)
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        text, keyboard = buy_random_num_menu(wof_info, user_balance, user_tickets, tickets_count)
        await call.message.edit_text(text, reply_markup=keyboard)


async def create_random_tickets(tickets_count):
    if tickets_count < 500:
        result = []
        for item in range(int(tickets_count)):
            ticket_num = random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
            while await db.check_ticket_in_db(ticket_num):
                ticket_num = random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
            result.append(ticket_num)
        return result
    else:
        possible_tickets = set(range(WOF_MIN_NUM, WOF_MAX_NUM + 1))
        purchased_tickets = await db.get_all_sold_tickets_nums()
        available_tickets = list(possible_tickets - purchased_tickets)
        return random.sample(available_tickets, tickets_count)


async def check_ticket_num(message, ticket_num):
    if not ticket_num.isdigit():
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_NUMBERS'), reply_markup=kb_del_msg())
        return True

    if len(ticket_num) > 7:
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_7_SYMBOL'), reply_markup=kb_del_msg())
        return True

    if await db.check_ticket_in_db(ticket_num):
        await message.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), reply_markup=kb_del_msg())
        return True

    return False


async def check_ticket_count(tickets_count):
    try:
        tickets_count = int(tickets_count)
    except ValueError:
        return True

    if tickets_count <= 0:
        return True

    return False


async def display_wof_info(user_id):
    wof_info = await db.get_active_wheel_info()
    user_balance = await db.get_user_balance(user_id, 'general')
    user_tickets = await db.get_count_user_tickets(user_id, 'all')
    return wof_info, user_balance, user_tickets


async def buy_winner_tickets(admin_id, winner_tickets_count, nonce):
    winner_tickets = []

    random.seed(nonce)
    winner_num = random.randint(WOF_MIN_NUM, WOF_MAX_NUM)
    if not await db.check_ticket_in_db(winner_num):
        winner_tickets.append(winner_num)

    while len(winner_tickets) != winner_tickets_count:
        rand_win_num = str(winner_num).replace(str(winner_num)[random.randint(0, 6)], str(random.randint(1, 9)))
        if not await db.check_ticket_in_db(rand_win_num):
            winner_tickets.append(rand_win_num)

    await db.add_new_ticket(admin_id, winner_tickets, 'random', time.time() + random.randint(172800, 1209600))
