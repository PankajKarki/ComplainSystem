from fastapi import APIRouter
from app.api.api_v1.endpoints import user, login, complaint

api_router = APIRouter()
api_router.include_router(login.auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user.user_router, prefix="/user", tags=["user"])
api_router.include_router(complaint.complain_router, prefix="/complaints", tags=["complaints"])
