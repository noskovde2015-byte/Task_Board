from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user
from core.config import settings
from core.models.user_model import User
from core.schemas.user_schema import UserRead

router = APIRouter(prefix=settings.prefix.users, tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
