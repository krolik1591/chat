from .deposit import router as d01_replenish_router
from .withdraw import router as d02_withdraw_router
from .withdraw_manual import router as d03_manual_withdraw_router

routers = [d01_replenish_router, d02_withdraw_router, d03_manual_withdraw_router]
