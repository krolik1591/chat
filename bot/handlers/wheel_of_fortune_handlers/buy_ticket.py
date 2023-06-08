from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext

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

    if await enter_ticket_num_check(message, ticket_num):
        return

    text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets, ticket_num)
    try:
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)
    except exceptions.TelegramBadRequest as e:
        print("User enter the same ticket num")

    await state.update_data(**{StateKeys.TICKET_NUM: ticket_num})


@router.callback_query(Text("buy_random_num"))
async def buy_random_ticket(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = buy_random_num_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_this_ticket"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):
    ticket_num = (await state.get_data()).get(StateKeys.TICKET_NUM)
    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    wof_info = await db.get_wheel_info()

    if user_balance < wof_info.ticket_cost:
        await call.answer(_('WOF_BUY_TICKET_ERR_NOT_ENOUGH_MONEY'), show_alert=True)
        return

    if await db.check_ticket_in_db(ticket_num):
        await call.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), show_alert=True)
        return

    with manager.pw_database.atomic():
        await db.add_new_ticket(call.from_user.id, ticket_num)
        await db.update_user_balance(call.from_user.id, 'general', -wof_info.ticket_cost)

    await call.answer(_('WOF_BUY_TICKET_SUCCESS'), show_alert=True)

    user_balance = await db.get_user_balance(call.from_user.id, 'general')
    user_tickets = await db.get_user_tickets(call.from_user.id)

    text, keyboard = buy_selected_num_menu(wof_info, user_balance, user_tickets, ticket_num)
    await call.message.edit_text(text, reply_markup=keyboard)



async def enter_ticket_num_check(message, ticket_num):
    if not ticket_num.isnumeric():
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_NUMBERS'), reply_markup=kb_del_msg())
        return True

    if len(ticket_num) != 7:
        await message.answer(_('WOF_BUY_TICKET_ERR_ENTER_ONLY_7_SYMBOL'), reply_markup=kb_del_msg())
        return True

    if await db.check_ticket_in_db(ticket_num):
        await message.answer(_('WOF_BUY_TICKET_ERR_THIS_TICKET_ALREADY_EXISTS'), reply_markup=kb_del_msg())
        return True


async def display_wof_info(user_id):
    wof_info = await db.get_wheel_info()
    user_balance = await db.get_user_balance(user_id, 'general')
    user_tickets = await db.get_user_tickets(user_id)
    return wof_info, user_balance, user_tickets
