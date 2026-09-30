from fastapi import APIRouter
from core.config import settings
from .auth_router import router as auth_router

router = APIRouter(prefix=settings.prefix.prefix)

router.include_router(auth_router)
