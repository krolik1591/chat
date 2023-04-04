from bot.handlers.games_handlers.m02_games import router as m02_games_router
from bot.handlers.games_handlers.m03_token import router as m03_token_router
from bot.handlers.games_handlers.m04_bets import router as m04_bets_router
from bot.handlers.games_handlers.m05_game_settings import router as m05_game_settings_router
from bot.handlers.games_handlers.m06_play_dice import router as m06_play_dice_router
from bot.handlers.games_handlers.m07_cube import router as m07_cube_router
from .m01_main import router as m01_main_router
from .other import router as other_router
from bot.handlers.deposit_handlers.d01_replenish import router as d01_replenish_router
from bot.handlers.deposit_handlers.d02_withdraw import router as d02_withdraw_router


routers = [
    m01_main_router, m02_games_router, m03_token_router,
    m04_bets_router, m05_game_settings_router,
    m06_play_dice_router, other_router, d01_replenish_router, d02_withdraw_router,
    m07_cube_router
]
