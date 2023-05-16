from aiogram.utils.i18n import gettext as _

from bot.consts import rewards
from bot.handlers.context import Context
from bot.handlers.games_handlers.dice_games import slots_check, texts as gtexts
from bot.handlers.games_handlers.dice_games.base_dice_game import Dice
from bot.handlers.states import Games, StateKeys


class DiceCube(Dice):
    EMOJI = "🎲"

    def get_text(self, context, dice_value, score_change, balance_icon):
        streak = context.state[StateKeys.CUBE_LOSE_STREAK]
        dice_number_emoji = gtexts.numbers_emoji(dice_value)
        cube_text = gtexts.cube_texts(streak)
        return cube_text.format(score_change=score_change, token_icon=balance_icon,
                                cube_lose_streak=streak, dice_number_emoji=dice_number_emoji)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        win = 0
        for user_bet in context.game_settings:
            if str(dice_value) in user_bet:
                if len(user_bet) == 1:
                    win += rewards.CubeRewards.EXACT_VALUE_BET
                if len(user_bet) == 2:
                    win += rewards.CubeRewards.BET_ON_RANGE
                if len(user_bet) == 3:
                    win += rewards.CubeRewards.BET_ON_PARITY
        return win

    def _get_score_change(self, context, dice_value):
        coefficient = self._get_coefficient(context, dice_value)
        return context.bet * (coefficient - len(context.game_settings))

    def pre_check(self, context: Context):
        if context.game_settings is None or len(context.game_settings or []) == 0:
            return _('GAME_ERR_BET_NOT_SELECTED')

        if context.bet * len(context.game_settings) > context.balance:
            return _('GAME_ERR_BET_TOO_BIG')


class DiceSlots(Dice):
    EMOJI = "🎰"

    def get_text(self, context, dice_value, score_change, balance_icon):
        if score_change == 0:
            return _('LOSE_TEXT')
        return _('WIN_TEXT').format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return slots_check.get_coefficient(dice_value, rewards.SLOTS_REWARDS)


class DiceBasket(Dice):
    EMOJI = "🏀"

    def get_text(self, context, dice_value, score_change, balance_icon):
        basket_text = gtexts.basket_texts(dice_value)
        return basket_text.format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return rewards.BASKET_REWARDS.get(dice_value, 0)


class DiceDarts(Dice):
    EMOJI = "🎯"

    def get_text(self, context, dice_value, score_change, balance_icon):
        darts_text = gtexts.darts_texts(dice_value)
        return darts_text.format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return rewards.DARTS_REWARDS.get(dice_value, 0)


class DiceBowling(Dice):
    EMOJI = "🎳"

    def get_text(self, context, dice_value, score_change, balance_icon):
        bowling_text = gtexts.bowling_texts(dice_value)
        return bowling_text.format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return rewards.BOWLING_REWARDS.get(dice_value, 0)


class DiceFootball(Dice):
    EMOJI = "⚽️"

    def get_text(self, context, dice_value, score_change, balance_icon):
        football_text = gtexts.football_texts(dice_value)
        return football_text.format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return rewards.FOOTBALL_REWARDS.get(dice_value, 0)


DICE_GAMES = {
    Games.CUBE: DiceCube(),
    Games.CASINO: DiceSlots(),
    Games.BASKET: DiceBasket(),
    Games.DARTS: DiceDarts(),
    Games.BOWLING: DiceBowling(),
    Games.FOOTBALL: DiceFootball(),
}
