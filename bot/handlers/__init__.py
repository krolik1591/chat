from .games_handlers import routers as game_routers
from .guides_handlers import routers as guides_routers
from .m01_main import router as m01_main_router

routers = [
    m01_main_router,
    * game_routers,
]
