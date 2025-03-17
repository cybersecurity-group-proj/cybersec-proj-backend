from fastapi import APIRouter

from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.post import post_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(post_router, prefix="/posts", tags=["Post"])


