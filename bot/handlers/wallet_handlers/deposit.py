from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.handlers.states import StateKeys
from bot.menus.wallet_menus.deposit_menu import deposit_menu

router = Router()


@router.callback_query(Text("replenish"))
async def replenish(call: types.CallbackQuery, state: FSMContext):
    user_wallet = await db.get_user_wallet(call.from_user.id)

    await state.update_data({StateKeys.ENTERED_DEPOSIT_AMOUNT: None})

    text, keyboard = deposit_menu(user_wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)
