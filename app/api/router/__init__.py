from fastapi import APIRouter
from core.config import settings
from .auth_router import router as auth_router
from .register_router import router as register_router
from .user_router import router as user_router

router = APIRouter(prefix=settings.prefix.prefix)

router.include_router(auth_router)
router.include_router(register_router)
router.include_router(user_router)
