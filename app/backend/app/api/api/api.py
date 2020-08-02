from fastapi import APIRouter

from app.api.api.routes import users, auth

api_router = APIRouter()

api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
