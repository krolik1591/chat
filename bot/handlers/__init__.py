from .games_handlers import routers as game_routers
from .guides_heandlers import routers as guides_routers
from .m01_main import router as m01_main_router
from .my_account_heandlers import routers as my_account_routers
from .other_handlers import routers as other_routers
from .wallet_handlers import routers as balance_routers
from .admin_handlers import routers as admin_routers
from .wheel_of_fortune_handlers import routers as wheel_routers

routers = [
    m01_main_router,
    * game_routers,
    * balance_routers,
    * my_account_routers,
    * guides_routers,
    * admin_routers,
    * wheel_routers,
    * other_routers      # other always may be last router
]
