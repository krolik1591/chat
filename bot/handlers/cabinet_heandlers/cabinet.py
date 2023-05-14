from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.other_handlers.ref import create_ref_link
from bot.menus.cabinet_menus.cabinet_menu import cabinet_menu
from bot.menus.cabinet_menus.referrals_menu import referrals_menu

router = Router()


@router.callback_query(text=["cabinet_menu"])
async def cabinet(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = cabinet_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["referrals_menu"])
async def referrals(call: types.CallbackQuery, state: FSMContext):
    invite_link = await create_ref_link(state, call.from_user.id)

    text, keyboard = referrals_menu(invite_link)
    await call.message.edit_text(text, reply_markup=keyboard)
