import time

from bot.db.methods import add_new_titan_tx
from bot.menus.deposit_menus.withdraw_menu.withdraw_titan_tx_menu import process_titan_tx_menu
from bot.utils.config_reader import config


async def process_titan_tx(user_id, username, ton_amount, context, token_id, user_withdraw_address):
    new_tx = await add_new_titan_tx(user_id=user_id, token_id=token_id, nano_ton_amount=ton_amount * 10**9,
                                    tx_address=user_withdraw_address, utime=int(time.time()))

    id_new_tx = new_tx.titanTXs_id

    text, keyboard = process_titan_tx_menu(user_id, username, ton_amount, id_new_tx)
    await context.fsm_context.bot.send_message(
        chat_id=config.admin_chat_id, text=text, reply_markup=keyboard)
