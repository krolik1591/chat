from bot.handlers.context import Context
from bot.handlers.states import Games, StateKeys
from bot.texts import GAME_ERR_BET_TOO_BIG, GAME_ERR_BET_NOT_SELECTED
from bot.utils.dice_check import dice_check_games, dice_check_texts
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
            return GAME_ERR_BET_TOO_BIG

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        raise NotImplementedError

    def _get_score_change(self, context: Context, dice_value: int) -> float:
        coefficient = self._get_coefficient(context, dice_value)
        return context.bet * (coefficient - 1)

    async def _update_lose_streak(self, context: Context, is_lose: bool):
        lose_streak = 0 if not is_lose else context.state.get(StateKeys.CUBE_LOSE_STREAK, 0) + 1
        await context.fsm_context.update_data(**{StateKeys.CUBE_LOSE_STREAK: lose_streak})
        context.state[StateKeys.CUBE_LOSE_STREAK] = lose_streak


class DiceCube(Dice):
    EMOJI = "🎲"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.cube(dice_value, score_change, balance_icon, context.state[StateKeys.CUBE_LOSE_STREAK])

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.cube(dice_value, context.game_settings)

    def _get_score_change(self, context, dice_value):
        coefficient = self._get_coefficient(context, dice_value)
        return context.bet * len(context.game_settings) * (coefficient - 1)

    def pre_check(self, context: Context):
        if context.game_settings is None or len(context.game_settings or []) == 0:
            return GAME_ERR_BET_NOT_SELECTED

        if context.bet * len(context.game_settings) > context.balance:
            return GAME_ERR_BET_TOO_BIG


class DiceSlots(Dice):
    EMOJI = "🎰"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.casino(dice_value, score_change, balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.slots(dice_value, context.game_settings)


class DiceBasket(Dice):
    EMOJI = "🏀"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.basket(dice_value, score_change, balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.basket(dice_value, context.game_settings)


class DiceDarts(Dice):
    EMOJI = "🎯"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.darts(dice_value, score_change, balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.darts(dice_value, context.game_settings)


class DiceBowling(Dice):
    EMOJI = "🎳"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.bowling(dice_value, score_change, balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.bowling(dice_value, context.game_settings)


class DiceFootball(Dice):
    EMOJI = "⚽️"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return dice_check_texts.football(dice_value, score_change, balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return dice_check_games.football(dice_value, context.game_settings)


DICE_GAMES = {
    Games.CUBE: DiceCube(),
    Games.CASINO: DiceSlots(),
    Games.BASKET: DiceBasket(),
    Games.DARTS: DiceDarts(),
    Games.BOWLING: DiceBowling(),
    Games.FOOTBALL: DiceFootball(),
}
