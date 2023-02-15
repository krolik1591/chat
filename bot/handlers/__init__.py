from .m01_main import router as m01_main_router
from .m02_games import router as m02_games_router
from .m03_token import router as m03_token_router
from .m04_bets import router as m04_bets_router
from .m05_game_settings import router as m05_game_settings_router
from .m06_play_dice import router as m06_play_dice_router
from .other import router as other_router

routers = [
    m01_main_router, m02_games_router, m03_token_router,
    m04_bets_router, m05_game_settings_router,
    m06_play_dice_router, other_router
]
