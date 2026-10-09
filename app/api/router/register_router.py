from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.user_schema import UserCreate
from core.models.db_helper import db_helper
from core.models.user_model import User
from core.config import settings
from auth.password_service import hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix=settings.prefix.register, tags=["Register"])


@router.post("")
async def register_user(
    user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await session.scalar(select(User).where(User.email == user_create.email))

    if user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_create.email,
        password=hash_password(user_create.password),
        username=user_create.username,
    )

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user
