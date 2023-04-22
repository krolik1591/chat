from bot.handlers.context import Context
from bot.handlers.games_handlers.dice_games import slots_check
from bot.handlers.games_handlers.dice_games.base_dice_game import Dice
from bot.consts.rewards import FOOTBALL_REWARDS, BOWLING_REWARDS, DARTS_REWARDS, \
    BASKET_REWARDS, \
    SLOTS_REWARDS, CubeRewards
from bot.handlers.games_handlers.dice_games.texts import FOOTBALL_TEXTS, BOWLING_TEXTS, DARTS_TEXTS, BASKET_TEXTS, \
    CUBE_TEXTS, \
    NUMBERS_EMOJI
from bot.handlers.states import Games, StateKeys
from bot.consts.texts import GAME_ERR_BET_TOO_BIG, GAME_ERR_BET_NOT_SELECTED, LOSE_TEXT, WIN_TEXT


class DiceCube(Dice):
    EMOJI = "🎲"

    def get_text(self, context, dice_value, score_change, balance_icon):
        streak = context.state[StateKeys.CUBE_LOSE_STREAK]
        dice_number_emoji = NUMBERS_EMOJI[dice_value]
        return CUBE_TEXTS[streak].format(score_change=score_change, token_icon=balance_icon,
                                         cube_lose_streak=streak, dice_number_emoji=dice_number_emoji)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        win = 0
        for user_bet in context.game_settings:
            if str(dice_value) in user_bet:
                if len(user_bet) == 1:
                    win += CubeRewards.EXACT_VALUE_BET
                if len(user_bet) == 2:
                    win += CubeRewards.BET_ON_RANGE
                if len(user_bet) == 3:
                    win += CubeRewards.BET_ON_PARITY
        return win

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
        if score_change == 0:
            return LOSE_TEXT
        return WIN_TEXT.format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return slots_check.get_coefficient(dice_value, SLOTS_REWARDS)


class DiceBasket(Dice):
    EMOJI = "🏀"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return BASKET_TEXTS[dice_value].format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return BASKET_REWARDS.get(dice_value, 0)


class DiceDarts(Dice):
    EMOJI = "🎯"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return DARTS_TEXTS[dice_value].format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return DARTS_REWARDS.get(dice_value, 0)


class DiceBowling(Dice):
    EMOJI = "🎳"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return BOWLING_TEXTS[dice_value].format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return BOWLING_REWARDS.get(dice_value, 0)


class DiceFootball(Dice):
    EMOJI = "⚽️"

    def get_text(self, context, dice_value, score_change, balance_icon):
        return FOOTBALL_TEXTS[dice_value].format(score_change=score_change, token_icon=balance_icon)

    def _get_coefficient(self, context: Context, dice_value: int) -> float:
        return FOOTBALL_REWARDS.get(dice_value, 0)


DICE_GAMES = {
    Games.CUBE: DiceCube(),
    Games.CASINO: DiceSlots(),
    Games.BASKET: DiceBasket(),
    Games.DARTS: DiceDarts(),
    Games.BOWLING: DiceBowling(),
    Games.FOOTBALL: DiceFootball(),
}
