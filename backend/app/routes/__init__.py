from fastapi import APIRouter
from .secret import router as secret_router
from .user import router as user_router

router = APIRouter()

router.include_router(secret_router, prefix="/secret")
router.include_router(user_router, prefix="/user")
