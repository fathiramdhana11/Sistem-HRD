from fastapi import APIRouter
from . import auth, users, menus, roles 
from . import role_menu_access
from . import user_action_logs

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(menus.router)
api_router.include_router(roles.router)
api_router.include_router(role_menu_access.router)
api_router.include_router(user_action_logs.router)