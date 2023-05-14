from .wallet_handlers import routers as balance_routers
from .games_handlers import routers as game_routers
from .m01_main import router as m01_main_router
from .other_handlers import routers as other_routers
from .cabinet_heandlers import routers as cabinet_routers
from .setting_heandlers import routers as setting_routers

routers = [
    m01_main_router,
    * game_routers,
    * balance_routers,
    * other_routers,
    * cabinet_routers,
    * setting_routers
]
