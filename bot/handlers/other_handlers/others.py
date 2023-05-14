from aiogram import Router, types
from aiogram.utils.deep_linking import create_start_link

from bot.handlers.states import Menu
from bot.utils.config_reader import config

router = Router()


@router.callback_query(text=["delete_message"])
async def delete_message(call: types.CallbackQuery):
    await call.message.delete()


@router.message(commands="admin")
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    is_admin = str(user_id) in config.admin_ids


@router.message(state=Menu.delete_message)
async def delete_message(message: types.Message):
    await message.delete()


@router.inline_query()
async def send_invite(query: types.InlineQuery, state):
    await query.answer([types.InlineQueryResultArticle(
        title='Send invitation', description='huihuihuihjughrtyjgrgri',
        id='wqweqweqwe', input_message_content=types.InputTextMessageContent(message_text='hi noggers'),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text='pohui', url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ])
