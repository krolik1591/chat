from bot.menus.deposit_menus.withdraw_menu.withdraw_titan_tx_menu import process_titan_tx_menu


async def process_titan_tx(user_id, username, ton_amount, context):
    text, keyboard = process_titan_tx_menu(user_id, username, ton_amount)
    await context.fsm_context.bot.send_message(
        chat_id=-886826963, text=text, reply_markup=keyboard)
