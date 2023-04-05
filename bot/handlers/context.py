from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import MIN_BET
from bot.handlers.states import StateKeys


class Context:

    @staticmethod
    async def from_fsm_context(user_id, fsm_context: FSMContext):
        state = await fsm_context.get_data()

        token_id = state.get(StateKeys.TOKEN_ID)
        balance = None
        if token_id:
            balance = await db.get_user_balance(user_id, token_id)

        return Context(user_id, fsm_context, state, balance)

    def __init__(self, user_id, fsm_context: FSMContext, state: dict, balance):
        self.user_id = user_id
        self.fsm_context = fsm_context
        self.state = state
        self.balance = balance

    @property
    def last_msg_id(self):
        return self.state.get(StateKeys.LAST_MSG_ID)

    @property
    def bet(self):
        return float(self.state.get(StateKeys.BET, MIN_BET))

    @property
    def token(self):
        token_id =  self.state.get(StateKeys.TOKEN_ID)
        if not token_id:
            return None
        return Token(token_id, self.state[StateKeys.TOKEN_ICON])

    @property
    def game(self):
        return self.state.get(StateKeys.GAME)

    @property
    def game_settings(self):
        return self.state.get(StateKeys.GAME_SETTINGS)


class Token:
    def __init__(self, id_, icon, price=None, balance=None):
        self.id = id_
        self.icon = icon
        self.price = price
        self.balance = balance

    @staticmethod
    def from_balance(balance):
        return Token(balance.token_id, balance.token_icon, balance.token_price, balance.balance)
