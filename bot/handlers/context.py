import json

from aiogram.dispatcher.fsm.context import FSMContext

from bot.db import db
from bot.consts.const import MIN_BET
from bot.handlers.states import StateKeys
from bot.utils.rounding import round_down


class Context:

    @staticmethod
    async def from_fsm_context(user_id, fsm_context: FSMContext):
        state = await fsm_context.get_data()
        balances = await db.get_user_balances(user_id)
        return Context(user_id, fsm_context, state, balances)

    def __init__(self, user_id, fsm_context: FSMContext, state: dict, balances: dict):
        self.user_id = user_id
        self.fsm_context = fsm_context
        self.state = state
        self.balances = balances

    @property
    def last_msg_id(self):
        return self.state.get(StateKeys.LAST_MSG_ID)

    @property
    def bet(self):
        return float(self.state.get(StateKeys.BET, MIN_BET))

    @property
    def balance_type(self):
        return self.state.get(StateKeys.BALANCE_TYPE)

    @property
    def balance(self):
        balance = self.balances[self.balance_type]
        return round_down(balance, 2)

    @property
    def game(self):
        return self.state.get(StateKeys.GAME)

    @property
    def game_settings(self):
        result = self.state.get(StateKeys.GAME_SETTINGS)
        if result is None:
            return None
        return json.loads(result)
