import json
import time

from bot.db.models import GameLog


# game logs


async def insert_game_log(user_id, balance_type, game_info, bet, result, game):
    # game = game name, ex: slots or mines or darts
    # game_info = ex:
    # slots/darts/...: {dice_result: 1-64}
    # dice: {dice_result: 1-6, dice_bet: 1-6 or 1-2 / 3-4 / 5/6 or even / odd}
    # mines: {mines_field: [], ...}
    # cuefa: {cuefa_bet: rock or paper or scissors}
    game_info = json.dumps(game_info)

    return await GameLog.create(user_id=user_id, balance_type=balance_type,
                                game=game, game_info=game_info,
                                bet=bet, result=result, timestamp=time.time())

