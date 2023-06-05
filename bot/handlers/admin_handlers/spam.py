from aiogram import Router, types, exceptions
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.admin_menus.spam_confirm_menu import approve_spam_msg
from bot.menus.admin_menus.spam_language_menu import spam_language_menu
from bot.menus.admin_menus.spam_type_menu import spam_type_menu
from bot.menus.utils import kb_del_msg
from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(Text("spam_type"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    text, kb = spam_type_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)


@router.callback_query(Text(startswith="who_get_spam_"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    spam_to = call.data.removeprefix('who_get_spam_')
    await state.update_data(**{StateKeys.WHO_GET_SPAM: spam_to})

    text, kb = spam_language_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)


@router.callback_query(Text(startswith="spam_lang"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.removeprefix("spam_lang")
    await state.update_data(**{StateKeys.SPAM_LANG: lang})

    await state.set_state(Menu.enter_spam_msg)

    await state.bot.edit_message_text(chat_id=call.from_user.id, text=_("ADMIN_SPAM_TEXT_ENTER_UR_MSG"),
                                      message_id=call.message.message_id)


@router.message(StateFilter(Menu.enter_spam_msg))
async def enter_spam_msg(message: Message, state: FSMContext):
    spam_msg_id = message.message_id
    await state.update_data(**{StateKeys.SPAM_MSG_ID: spam_msg_id})

    await state.bot.send_message(message.from_user.id, _('ADMIN_SPAM_TEXT_TEMPLATE'))

    await state.bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                                 message_id=spam_msg_id, reply_markup=kb_del_msg())

    text, kb = approve_spam_msg()
    await state.bot.send_message(message.from_user.id, text, reply_markup=kb)


@router.callback_query(Text(startswith="spam_sending_"))
async def spam_sending(call: types.CallbackQuery, state: FSMContext):
    spam_confirm = call.data.removeprefix("spam_sending_")
    who_receive_spam = (await state.get_data()).get(StateKeys.WHO_GET_SPAM)

    if bool(spam_confirm):
        spam_msg_id = (await state.get_data()).get(StateKeys.SPAM_MSG_ID)

        if who_receive_spam == 'all':
            lang_receiver = (await state.get_data()).get(StateKeys.SPAM_LANG)
            users = await db.get_users_by_lang(lang_receiver)
            if len(users) == 0:
                await call.answer(_("ADMIN_SPAM_ANSWER_USERS_NOT_FOUND"), show_alert=True)
                text, kb = spam_language_menu()
                await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)
                return

            for user in users:
                try:
                    try:
                        await state.bot.copy_message(chat_id=user, from_chat_id=call.from_user.id,
                                                     message_id=spam_msg_id, reply_markup=kb_del_msg())
                    except exceptions.TelegramForbiddenError:
                        await db.user_blocked_bot(user)
                        print(f"User with id: {user} are block bot.")

                except exceptions.TelegramBadRequest:
                    print(f"User with id: {user} are doesnt exist.")
