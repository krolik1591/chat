from aiogram.dispatcher.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    bet = State()
    withdraw_amount = State()
    withdraw_amount_approve = State()
    withdraw_address = State()


LAST_MSG_ID = 'last_msg_id'
BET = 'bet'
TOKEN_ID = 'token_id'
TOKEN_ICON = 'token_icon'
GAME = 'game'
GAME_SETTINGS = 'game_settings'

# todo replace with GAME_SETTINGS
CUBE_BET = 'cube_bet'
