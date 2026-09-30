from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token,
)
from auth.password_service import authenticate_user
from core.models.db_helper import db_helper
from core.schemas.user_schema import UserAuth
from core.config import settings

router = APIRouter(prefix=settings.prefix.login, tags=["Login"])


@router.post("/")
async def login(
    user_data: UserAuth,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
        session=session,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token()
    await save_refresh_token(user_id=user.id, token=refresh_token, session=session)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )
    return {"detail": "Successfully logged in."}
