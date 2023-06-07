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
