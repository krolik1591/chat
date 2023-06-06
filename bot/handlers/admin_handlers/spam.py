from asyncio import sleep

from aiogram import Router, types, exceptions
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.admin_menus.admin_menu import admin_menu
from bot.menus.admin_menus.spam_menus.confirm_menu import approve_spam_msg
from bot.menus.admin_menus.spam_menus.language_receiver_menu import spam_language_menu
from bot.menus.admin_menus.spam_menus.category_for_spam_menu import spam_type_menu
from bot.menus.main_menus.language_menu import LANGUAGES
from bot.menus.utils import kb_del_msg, kb_del_msg_for_spam
from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(Text("spam_type"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    text, kb = spam_type_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)


@router.callback_query(Text(startswith="who_get_spam_"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    spam_type = call.data.removeprefix('who_get_spam_')
    await state.update_data(**{StateKeys.SPAM_TYPE: spam_type})

    text, kb = spam_language_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)


@router.callback_query(Text(startswith="spam_lang"))
async def choose_spam(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.removeprefix("spam_lang")
    await state.update_data(**{StateKeys.SPAM_LANG: lang})

    spam_type = (await state.get_data()).get(StateKeys.SPAM_TYPE)
    if spam_type == 'for_id':
        await state.bot.edit_message_text(_('ADMIN_SPAM_TEXT_ENTER_RECEIVER_ID)'), call.from_user.id, call.message.message_id)
        await state.set_state(Menu.get_id_spam_receiver)
    else:
        await state.set_state(Menu.enter_spam_msg)
        await state.bot.edit_message_text(chat_id=call.from_user.id, text=_("ADMIN_SPAM_TEXT_ENTER_UR_MSG"),
                                          message_id=call.message.message_id)


@router.message(StateFilter(Menu.get_id_spam_receiver))
async def get_id_spam_receiver(message: Message, state: FSMContext):
    await message.delete()

    id_receivers = message.text.split(',')
    receiver = []
    not_exist_receiver = ''
    another_lang_receiver = {}
    lang_receiver = (await state.get_data()).get(StateKeys.SPAM_LANG)
    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)

    for user_id in id_receivers:
        try:
            user_lang = await db.get_user_lang(user_id)
            if user_lang == lang_receiver:
                receiver.append(user_id)
            else:
                another_lang_receiver[user_id] = user_lang

        except ValueError:
            not_exist_receiver += user_id + ','

    if not_exist_receiver or another_lang_receiver:
        text = get_text_for_incorrect_receiver(lang_receiver, another_lang_receiver)
        await state.bot.send_message(message.from_user.id, _("ADMIN_SPAM_TEXT_WHICH_USER_DOESNT_EXIST").
                                     format(not_exist_receiver=not_exist_receiver, another_lang=text),
                                     reply_markup=kb_del_msg())

    if not receiver:
        await message.answer(_('ADMIN_SPAM_TEXT_NO_USER_FOUND_ID_IN_BD'), reply_markup=kb_del_msg())
        text, kb = spam_type_menu()
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=kb)
        return

    await state.update_data(**{StateKeys.ID_RECEIVERS: receiver})
    await state.set_state(Menu.enter_spam_msg)
    await state.bot.edit_message_text(chat_id=message.from_user.id, text=_("ADMIN_SPAM_TEXT_ENTER_UR_MSG"),
                                      message_id=last_msg_id)


@router.message(StateFilter(Menu.enter_spam_msg))
async def enter_spam_msg(message: Message, state: FSMContext):
    spam_msg_id = message.message_id
    await state.update_data(**{StateKeys.SPAM_MSG_ID: spam_msg_id})

    await state.bot.send_message(message.from_user.id, _('ADMIN_SPAM_TEXT_TEMPLATE'))

    await state.bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                                 message_id=spam_msg_id)

    text, kb = approve_spam_msg()
    msg = await state.bot.send_message(message.from_user.id, text, reply_markup=kb)
    await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})


@router.callback_query(Text(startswith="spam_sending_"))
async def spam_sending(call: types.CallbackQuery, state: FSMContext):
    spam_confirm = call.data.removeprefix("spam_sending_")
    if not spam_confirm:
        text, kb = spam_type_menu()
        await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)
        await state.set_state(Menu.delete_message)
        return

    data = await state.get_data()
    spam_msg_id = data.get(StateKeys.SPAM_MSG_ID)
    id_receiver = data.get(StateKeys.ID_RECEIVERS)
    lang_receiver = data.get(StateKeys.SPAM_LANG)
    spam_type = data.get(StateKeys.SPAM_TYPE)

    if spam_type == 'all':
        users = await db.get_users_by_lang(lang_receiver)

        if not users:
            await call.answer(_("ADMIN_SPAM_ANSWER_USERS_NOT_FOUND").format(lang=lang_receiver), show_alert=True)
            text, kb = spam_language_menu()
            await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)
            return

        await send_spam_msg(call, state, users, spam_msg_id)

    else:
        sending_failed_id = await send_spam_msg(call, state, id_receiver, spam_msg_id)
        if sending_failed_id:
            text = '\n'.join(str(failed_id) for failed_id in sending_failed_id)
            await state.bot.send_message(call.from_user.id, _("ADMIN_SPAM_WHO_DOESNT_RECEIVE_SPAM").format(text),
                                         reply_markup=kb_del_msg())

    text, kb = admin_menu()
    await state.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=kb)
    await state.set_state(Menu.delete_message)


async def send_spam_msg(call, state, users, spam_msg_id):
    sending_failed_id = []
    for user in users:
        try:
            await state.bot.copy_message(chat_id=user, from_chat_id=call.from_user.id,
                                         message_id=spam_msg_id, reply_markup=kb_del_msg_for_spam())
        except exceptions.TelegramRetryAfter as e:
            sending_failed_id.append(user)
            print("So much messages. Need to sleep 10 sec")
            await sleep(e.retry_after)

        except exceptions.TelegramForbiddenError:
            sending_failed_id.append(user + 'is blocked bot')
            await db.user_blocked_bot(user)
            print(f"User with id: {user} are block bot.")

        except exceptions.TelegramBadRequest:
            sending_failed_id.append(user + 'is doesent exist')
            print(f"User with id: {user} are doesnt exist.")

    return sending_failed_id


def get_text_for_incorrect_receiver(lang_receiver, another_lang_receiver):
    res = {}
    text = ''
    for lang in LANGUAGES:
        if lang == lang_receiver:
            continue
        res[lang] = ''

    for user_id_, user_lang_ in another_lang_receiver.items():
        res[user_lang_] = user_id_ + ','

    for _user_lang, _user_id in res.items():
        text += _user_lang + ': ' + _user_id + "\n"

    return text
