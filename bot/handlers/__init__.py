from .deposit_handlers import routers as balance_routers
from .games_handlers import routers as game_routers
from .m01_main import router as m01_main_router
from .other_handlers import routers as other_routers

routers = [
    m01_main_router,
    * game_routers,
    * balance_routers,
    * other_routers
]
