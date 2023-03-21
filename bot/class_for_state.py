from aiogram.dispatcher.fsm.state import State, StatesGroup


class Choosen_message(StatesGroup):
    choosing_bet = State()
    choosing_withdraw_amount = State()
    choosing_withdraw_address = State()
