# File: backend/app/api/routes/api_router.py

from fastapi import APIRouter
from . import auth, users, menus

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(menus.router)