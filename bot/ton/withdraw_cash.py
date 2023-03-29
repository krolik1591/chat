from bot.menus.deposit_menus.withdraw_menu.withdraw_condition_menu import withdraw_condition_menu
from bot.menus.deposit_menus.withdraw_menu.withdraw_menu_err import withdraw_menu_err
from bot.ton.process_withdraw_tx import process_withdraw_tx


async def withdraw_cash_to_user(master_wallet, user_withdraw_address, withdraw_amount_ton, user_id, token, state):
    master_balance_nano = await master_wallet.get_balance()
    master_balance_ton = master_balance_nano / 1e9
    print(master_balance_ton, withdraw_amount_ton)
    print('mw address', master_wallet.address)

    if master_balance_ton > withdraw_amount_ton:

        transfer_application = await master_wallet.transfer_ton(user_withdraw_address, withdraw_amount_ton)
        print('transfer_application:', transfer_application)

        withdraw_condition = await process_withdraw_tx(state, user_withdraw_address, withdraw_amount_ton, user_id,
                                                       token, master_wallet.address)

        text, keyboard = withdraw_condition_menu(withdraw_condition)    # transfer money approve
        await state.bot.send_message(text=text, reply_markup=keyboard, chat_id=user_id)

    else:
        last_msg = (await state.get_data()).get('last_msg_id')

        text, keyboard = withdraw_menu_err(6)  # not enough money on master wallet
        await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=user_id, message_id=last_msg)
