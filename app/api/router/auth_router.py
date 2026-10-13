from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    save_refresh_token,
    hash_refresh_token,
)
from auth.password_service import authenticate_user
from core.models.db_helper import db_helper
from core.models.refresh_token import RefreshToken
from core.schemas.user_schema import UserAuth
from core.config import settings

router = APIRouter(prefix=settings.prefix.login, tags=["Login"])


@router.post("")
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


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        hashed = hash_refresh_token(refresh_token)

        stmt = select(RefreshToken).where(RefreshToken.token_hash == hashed)
        result = await session.execute(stmt)
        token = result.scalar_one_or_none()

        if token:
            await session.delete(token)
            await session.commit()

    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")

    return {"message": "Logged out"}
