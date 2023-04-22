from .m02_games import router as m02_games_router
from .m03_balance import router as m03_balance_router
from .m04_game_settings import router as m05_game_settings_router
from .m05_bets import router as m04_bets_router
from .m06_play_dice import router as m06_play_dice_router

routers = [m02_games_router, m03_balance_router, m04_bets_router, m05_game_settings_router, m06_play_dice_router]
