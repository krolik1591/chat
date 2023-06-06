from asyncio import sleep
from collections import defaultdict

from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.admin_menus import admin_menu, approve_spam_msg, spam_language_menu, spam_type_menu
from bot.menus.utils import kb_del_msg, kb_del_msg_for_spam

router = Router()


@router.callback_query(Text("spam_type"))
async def choose_spam_type(call: types.CallbackQuery):
    text, kb = spam_type_menu()
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith="who_get_spam_"))
async def choose_spam_callback(call: types.CallbackQuery, state: FSMContext):
    spam_type = call.data.removeprefix('who_get_spam_')
    await state.update_data(**{StateKeys.SPAM_TYPE: spam_type})

    text, kb = spam_language_menu()
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith="spam_lang"))
async def choose_spam_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.removeprefix("spam_lang")
    await state.update_data(**{StateKeys.SPAM_LANG: lang})

    spam_type = (await state.get_data()).get(StateKeys.SPAM_TYPE)
    if spam_type == 'for_id':
        await call.message.edit_text(_('ADMIN_SPAM_TEXT_ENTER_RECEIVER_ID)'))
        await state.set_state(Menu.get_id_spam_receiver)
    else:
        await call.message.edit_text(_("ADMIN_SPAM_TEXT_ENTER_UR_MSG"))
        await state.set_state(Menu.enter_spam_msg)


@router.message(StateFilter(Menu.get_id_spam_receiver))
async def enter_spam_receivers_id(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    lang_receiver = data[StateKeys.SPAM_LANG]
    last_msg_id = data[StateKeys.LAST_MSG_ID]

    receivers_id = [i.strip() for i in message.text.split(',')]
    not_exist_receivers = []
    another_lang_receivers = []
    normal_receivers = []

    for user_id in receivers_id:
        try:
            user_lang = await db.get_user_lang(user_id)
            if user_lang == lang_receiver:
                normal_receivers.append(user_id)
            else:
                another_lang_receivers.append((user_id, user_lang))

        except ValueError:
            not_exist_receivers.append(user_id)

    if not_exist_receivers or another_lang_receivers:
        not_exist_text = ', '.join(not_exist_receivers)
        another_lang_text = get_text_for_incorrect_receivers(another_lang_receivers)
        text = _("ADMIN_SPAM_TEXT_WHICH_USER_DOESNT_EXIST").format(not_exist_receiver=not_exist_text,
                                                                   another_lang=another_lang_text)
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=kb_del_msg())

    if not normal_receivers:
        await message.answer(_('ADMIN_SPAM_TEXT_NO_USER_FOUND_ID_IN_BD'), reply_markup=kb_del_msg())
        text, kb = spam_type_menu()
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=kb)
        return

    await state.update_data(**{StateKeys.ID_RECEIVERS: normal_receivers})
    await state.set_state(Menu.enter_spam_msg)
    msg = await message.answer(text=_("ADMIN_SPAM_TEXT_ENTER_UR_MSG"))
    await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})


@router.message(StateFilter(Menu.enter_spam_msg))
async def enter_spam_msg(message: Message, state: FSMContext):
    spam_msg_id = message.message_id
    await state.update_data(**{StateKeys.SPAM_MSG_ID: spam_msg_id})

    await message.answer(_('ADMIN_SPAM_TEXT_TEMPLATE'))
    await message.copy_to(message.chat.id)

    text, kb = approve_spam_msg()
    msg = await message.answer(text, reply_markup=kb)
    await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})


@router.callback_query(Text(startswith="spam_sending_"))
async def spam_sending(call: types.CallbackQuery, state: FSMContext):
    spam_confirm = call.data.removeprefix("spam_sending_")
    if not spam_confirm:
        text, kb = spam_type_menu()
        await call.message.edit_text(text, reply_markup=kb)
        await state.set_state(Menu.delete_message)
        return

    data = await state.get_data()
    spam_msg_id = data[StateKeys.SPAM_MSG_ID]
    lang_receiver = data[StateKeys.SPAM_LANG]
    spam_type = data[StateKeys.SPAM_TYPE]

    if spam_type == 'all':
        users = await db.get_users_by_lang(lang_receiver)

        if not users:
            await call.answer(_("ADMIN_SPAM_ANSWER_USERS_NOT_FOUND").format(lang=lang_receiver), show_alert=True)
            text, kb = spam_language_menu()
            await call.message.edit_text(text, reply_markup=kb)
            return

        await send_spam_msg(call, state, users, spam_msg_id)

    elif spam_type == "for_id":
        receivers = data[StateKeys.ID_RECEIVERS]
        errors = await send_spam_msg(call, state, receivers, spam_msg_id)
        if errors:
            await call.message.edit_text(_("ADMIN_SPAM_WHO_DOESNT_RECEIVE_SPAM").format('\n'.join(errors)),
                                         reply_markup=kb_del_msg())

    else:
        raise Exception("Incorrect spam_type " + spam_type)

    text, kb = admin_menu()
    await call.message.edit_text(text, reply_markup=kb)
    await state.set_state(Menu.delete_message)


async def send_spam_msg(call, state, users, spam_msg_id):
    errors = []
    for user in users:
        error = await set_spam_msg_(state.bot, (call.from_user.id, spam_msg_id), user)
        if error is not None:
            print(error)
            errors.append(error)

    return errors


async def set_spam_msg_(bot, spam_msg, receiver_id):
    for i in range(5):
        try:
            await bot.copy_message(from_chat_id=spam_msg[0], message_id=spam_msg[1],
                                   chat_id=receiver_id, reply_markup=kb_del_msg_for_spam())
            return None  # no errors!
        except exceptions.TelegramRetryAfter as e:
            print(f"So much messages. Need to sleep {e.retry_after} sec")
            await sleep(e.retry_after)
            continue

        except exceptions.TelegramForbiddenError:
            await db.user_blocked_bot(receiver_id)
            return f"{receiver_id} blocked the bot"

        except exceptions.TelegramBadRequest:
            return f"{receiver_id} doesn't exist"

    else:
        return f"{receiver_id} flood limit"


def get_text_for_incorrect_receivers(another_lang_receivers):
    res = defaultdict(list)
    for user_id, user_lang in another_lang_receivers:
        res[user_lang].append(user_id)

    return "\n".join([
        lang + ": " + '\n'.join(users)
        for lang, users in res.items()
    ])
