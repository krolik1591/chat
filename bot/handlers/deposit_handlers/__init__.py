from .d01_replenish import router as d01_replenish_router
from .d02_withdraw import router as d02_withdraw_router
from .d03_manual_withdraw import router as d03_manual_withdraw_router

routers = [d01_replenish_router, d02_withdraw_router, d03_manual_withdraw_router]
