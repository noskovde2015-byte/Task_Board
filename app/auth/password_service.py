import bcrypt
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if (
        not user
        or not user.hashed_password
        or not verify_password(password, user.hashed_password)
    ):
        return None
    return user
