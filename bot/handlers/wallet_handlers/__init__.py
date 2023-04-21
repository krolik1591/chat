from .wallet import router as wallet_router
from .deposit import router as deposit_router
from .withdraw import router as withdraw_router
from .withdraw_manual import router as manual_withdraw_router

routers = [wallet_router, deposit_router, withdraw_router, manual_withdraw_router]
