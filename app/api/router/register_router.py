from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.password_service import hash_password
from core.config import settings
from core.models.db_helper import db_helper
from core.models.user_model import User
from core.schemas.user_schema import UserCreate, UserRead

router = APIRouter(prefix=settings.prefix.register, tags=["Register"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(User).where(
        (User.email == user_create.email) | (User.username == user_create.username)
    )
    existing_user = await session.scalar(stmt)

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email or username already taken")

    new_user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
    )
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Email or username already taken")

    await session.refresh(new_user)
    return new_user
