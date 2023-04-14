from bot.menus.deposit_menus.withdraw_menu.withdraw_titan_tx_menu import process_titan_tx_menu
from bot.utils.config_reader import config


async def process_titan_tx(user_id, username, ton_amount, context):
    text, keyboard = process_titan_tx_menu(user_id, username, ton_amount)
    await context.fsm_context.bot.send_message(
        chat_id=config.admin_chat_id, text=text, reply_markup=keyboard)
