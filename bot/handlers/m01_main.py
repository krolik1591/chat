from TonTools.Contracts.Wallet import Wallet
from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.consts.const import START_POINTS
from bot.db import db
from bot.handlers.context import Context
from bot.handlers.states import Menu, StateKeys
from bot.menus import main_menu
from bot.menus.utils import kb_del_msg
from bot.tokens.token_ton import TonWrapper

flags = {"throttling_key": "default"}
router = Router()


async def send_main_menu(context: Context, msg_id=None):
    balances = await db.get_user_balances(context.user_id)
    lang = await db.get_user_lang(context.user_id)
    text, keyboard = main_menu(balances, lang)

    if msg_id is None:
        msg = await context.fsm_context.bot.send_message(context.user_id, text, reply_markup=keyboard)
        await context.fsm_context.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})
    else:
        await context.fsm_context.bot.edit_message_text(
            chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    await context.fsm_context.set_state(Menu.delete_message)


@router.message(F.chat.type == "private", Command("start"), flags=flags)
async def cmd_start(message: Message, state: FSMContext, i18n_middleware):

    try:
        user_lang = await db.get_user_lang(message.from_user.id)

        # todo only if blocked
        await db.user_blocked_bot(message.from_user.id, False)
        await db.set_user_last_active(message.from_user.id)

        await i18n_middleware.set_locale(state, user_lang)

    except ValueError:
        invite_sender = None
        if len(message.text.split()) == 2:
            try:
                invite_sender = int(message.text.split()[1])
                await db.get_user_lang(invite_sender)
            except ValueError:
                await message.answer(_('CHECK_REF_DENIED_TEXT'))
                return

            user_lang = await db.get_user_lang(invite_sender)
            await i18n_middleware.set_locale(state, user_lang)
            kb = kb_del_msg()
            await state.bot.send_message(invite_sender, _('CHECK_REF_APPROVE_TEXT').
                                         format(id=message.from_user.id, name=message.from_user.first_name),
                                         reply_markup=kb)

        await db.create_new_user(message.from_user.id, message.from_user.username, invite_sender, START_POINTS)

        new_wallet = Wallet(provider=TonWrapper.INSTANCE)
        mnemonics = ','.join(new_wallet.mnemonics)
        await db.create_user_wallet(message.from_user.id, new_wallet.address, mnemonics)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await send_main_menu(context)


@router.callback_query(Text("main_menu"))
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await send_main_menu(context, msg_id=call.message.message_id)
