from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import START_POINTS
from bot.handlers.main import cmd_start

router = Router()


@router.callback_query(text=["end_money"])
async def demo_money(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(balance=START_POINTS)
    await call.answer('Людяність відновлена')

    await cmd_start(call.message, state)
    await call.message.delete()
