from .auth import router as auth_router
from .content import router as content_router
from .sync import router as sync_router
from .progress import router as progress_router
from .admin import router as admin_router
from .remote_bridge import router as remote_bridge_router

__all__ = [
    "auth_router",
    "content_router",
    "sync_router",
    "progress_router",
    "admin_router",
    "remote_bridge_router",
]
