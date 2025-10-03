"""
Routers package
"""
from . import (
    auth_router as auth, 
    user_router,
    exercise_router,
    routine_router,
    nutrition_router,
    progress_router,
    notification_router,
    motivation_router
)

__all__ = [
    "auth", 
    "user_router", 
    "exercise_router", 
    "routine_router", 
    "nutrition_router",
    "progress_router",
    "notification_router",
    "motivation_router"
]