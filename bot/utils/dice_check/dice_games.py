from bot.handlers.context import Context
from bot.handlers.states import Games, StateKeys
from bot.menus.utils import get_balance_icon
from bot.texts import GAME_ERR_BET_TOO_BIG, GAME_ERR_BET_NOT_SELECTED
from bot.utils.dice_check import dice_check_games, dice_check_texts
from bot.utils.rounding import round_down


class Dice:
    def __init__(self, dice_emoji, calc_res_func, text_func):
        self.dice_emoji = dice_emoji
        self.calc_res_func = calc_res_func
        self.text_func = text_func

    async def get_result(self, dice_value, context):
        coefficient = self.calc_res_func(dice_value, context.game_settings)
        score_change = round_down((coefficient * context.bet), 5)
        user_win = round_down(score_change - context.bet, 5)
        game_info = {"dice_result": dice_value, "game_settings": context.game_settings}

        balance_icon = get_balance_icon(context.balance_type)
        text = self.text_func(dice_value, round_down(score_change, 2), balance_icon)

        return {
            'coefficient': coefficient,
            'score_change': score_change,
            'user_win': user_win,
            'game_info': game_info,
            'text': text
        }

    def pre_check(self, context: Context):
        if context.bet > context.balance:
            return "Ставка більше балансу"


class DiceCube(Dice):
    async def get_result(self, dice_value, context):
        coefficient = self.calc_res_func(dice_value, context.game_settings)
        score_change = round_down((coefficient * context.bet), 5)
        user_win = round_down(score_change - context.bet * len(context.game_settings), 5)
        game_info = {"dice_result": dice_value, "game_settings": context.game_settings}

        lose_streak = 0 if coefficient != 0 else context.state.get(StateKeys.CUBE_LOSE_STREAK, 0) + 1
        await context.fsm_context.update_data(**{StateKeys.CUBE_LOSE_STREAK: lose_streak + 1})

        balance_icon = get_balance_icon(context.balance_type)
        text = self.text_func(dice_value, round_down(score_change, 2), balance_icon, lose_streak)

        return {
            'coefficient': coefficient,
            'score_change': score_change,
            'user_win': user_win,
            'game_info': game_info,
            'text': text
        }

    def pre_check(self, context: Context):
        super_result = super().pre_check(context)
        if super_result is not None:
            return super_result

        if context.bet * len(context.game_settings or []) > context.balance:
            return GAME_ERR_BET_TOO_BIG

        if context.game_settings is None or len(context.game_settings) == 0:
            return GAME_ERR_BET_NOT_SELECTED


DICE_GAMES = {
    Games.CUBE: DiceCube("🎲", dice_check_games.cube, dice_check_texts.cube),
    Games.CASINO: Dice("🎰", dice_check_games.slots, dice_check_texts.casino),
    Games.BASKET: Dice("🏀", dice_check_games.basket, dice_check_texts.basket),
    Games.DARTS: Dice("🎯", dice_check_games.darts, dice_check_texts.darts),
    Games.BOWLING: Dice("🎳", dice_check_games.bowling, dice_check_texts.bowling),
    Games.FOOTBALL: Dice("⚽️", dice_check_games.football, dice_check_texts.football),

}

