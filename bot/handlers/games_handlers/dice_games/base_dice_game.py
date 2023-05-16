from bot.handlers.context import Context
from bot.handlers.states import StateKeys
from bot.utils.rounding import round_down

from aiogram.utils.i18n import gettext as _

from bot.handlers.context import Context
from bot.handlers.states import StateKeys
from bot.utils.rounding import round_down


class Dice:
    EMOJI = "?"

    async def get_result(self, context: Context, dice_value: int):
        score_change = self._get_score_change(context, dice_value)
        game_info = {"dice_result": dice_value, "game_settings": context.game_settings}

        await self._update_lose_streak(context, score_change <= 0)

        return {
            'score_change': round_down(score_change, 5),
            'game_info': game_info,
        }

    def get_text(self, context, dice_value, score_change, balance_icon):
        raise NotImplementedError

    def pre_check(self, context: Context):
        if context.bet > context.balance:
            return _('GAME_ERR_BET_TOO_BIG')

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        raise NotImplementedError

    def _get_score_change(self, context: Context, dice_value: int) -> float:
        coefficient = self._get_coefficient(context, dice_value)
        return context.bet * (coefficient - 1)

    async def _update_lose_streak(self, context: Context, is_lose: bool):
        lose_streak = 0 if not is_lose else context.state.get(StateKeys.CUBE_LOSE_STREAK, 0) + 1
        await context.fsm_context.update_data(**{StateKeys.CUBE_LOSE_STREAK: lose_streak})
        context.state[StateKeys.CUBE_LOSE_STREAK] = lose_streak
