from bot.db.methods import update_user_balance
from bot.menus.deposit_menus.withdraw_menu.withdraw_condition_menu import withdraw_condition_menu
from bot.menus.deposit_menus.withdraw_menu.withdraw_menu_err import withdraw_menu_err
from bot.ton.process_withdraw_tx import process_withdraw_tx


async def withdraw_cash_to_user(master_wallet, user_withdraw_address, withdraw_amount_ton, user_id, token, state):
    withdraw_amount_price = withdraw_amount_ton * token.price

    master_balance_nano = await master_wallet.get_balance()
    master_balance_ton = master_balance_nano / 1e9

    if master_balance_ton > withdraw_amount_ton:
        await master_wallet.transfer_ton(user_withdraw_address, withdraw_amount_ton)

        withdraw_condition = await process_withdraw_tx(state, user_withdraw_address, withdraw_amount_ton, user_id,
                                                       master_wallet.address)

        await withdraw_approve(withdraw_condition, state, user_id, token, withdraw_amount_price)

    else:
        await update_user_balance(user_id, token.token_id, withdraw_amount_price)

        text_err, keyboard = withdraw_menu_err(6)  # not enough money on master wallet
        await state.bot.send_message(user_id, text_err, reply_markup=keyboard)


async def withdraw_approve(withdraw_condition, state, user_id, token, withdraw_amount_price):
    if withdraw_condition:
        text, keyboard = withdraw_condition_menu(withdraw_condition)  # transfer money approve
        await state.bot.send_message(text=text, reply_markup=keyboard, chat_id=user_id)
    else:
        await update_user_balance(user_id, token.token_id, withdraw_amount_price)
        text, keyboard = withdraw_condition_menu(withdraw_condition)
        await state.bot.send_message(text=text, reply_markup=keyboard, chat_id=user_id)
