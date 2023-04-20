from aiogram import Router, types

router = Router()


@router.callback_query(text=["delete_message"])
async def delete_message(call: types.CallbackQuery):
    await call.message.delete()
