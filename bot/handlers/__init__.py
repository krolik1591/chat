from .games_handlers import routers as game_routers
from .m01_main import router as m01_main_router
from .games import router as games_router

routers = [
    games_router,
    m01_main_router,
    * game_routers,
]
