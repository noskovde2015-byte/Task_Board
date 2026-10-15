from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.board_model import Board
from core.models.board_member import BoardMember
from core.models.user_model import User


async def get_my_boards(current_user: User, session: AsyncSession) -> Sequence[Board]:
    stmt = (
        select(Board)
        .join(BoardMember, BoardMember.board_id == Board.id)
        .where(BoardMember.user_id == current_user.id)
        .order_by(Board.id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
