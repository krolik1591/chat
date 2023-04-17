import logging
import time

from aiogram.exceptions import TelegramMigrateToChat

from bot.db.db import manager
from bot.db.methods import add_new_titan_tx, update_user_balance
from bot.menus.deposit_menus.withdraw_menu.withdraw_titan_tx_menu import process_titan_tx_menu
from bot.utils.config_reader import config


async def process_titan_tx(user_id, username, ton_amount, context, token, user_withdraw_address):
    with manager.pw_database.atomic():
        new_tx = await add_new_titan_tx(user_id=user_id, nano_ton_amount=ton_amount * 10**9, token_id=token.token_id,
                                        price=token.price, tx_address=user_withdraw_address, utime=int(time.time()))
        id_new_tx = new_tx.titanTXs_id

        text, keyboard = process_titan_tx_menu(user_id, username, ton_amount, id_new_tx)
        try:
            await context.fsm_context.bot.send_message(
                chat_id=config.admin_chat_id, text=text, reply_markup=keyboard)
        except TelegramMigrateToChat as ex:
            logging.exception('User trying withdraw cash')
            return

        await update_user_balance(user_id, token.token_id, -ton_amount * token.price)
