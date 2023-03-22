from aiogram.dispatcher.fsm.state import State, StatesGroup


class Choosen_message(StatesGroup):
    bet = State()
    withdraw_amount = State()
    withdraw_amount_approve = State()
    withdraw_address = State()
