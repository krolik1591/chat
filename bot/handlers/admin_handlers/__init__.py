from .admin import router as admin_router
from .spam import router as spam_router

routers = [admin_router, spam_router]
