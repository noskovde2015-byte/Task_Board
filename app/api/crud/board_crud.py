from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models.board_column_model import BoardColumn
from core.models.board_model import Board
from core.models.board_member import BoardMember, BoardRole
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


DEFAULT_COLUMNS = ["To Do", "In Progress", "Done"]


async def create_new_board(
    title: str, is_public: bool, current_user: User, session: AsyncSession
) -> Board:
    new_board = Board(title=title, is_public=is_public, owner_id=current_user.id)
    session.add(new_board)
    await session.flush()

    session.add(
        BoardMember(
            board_id=new_board.id, user_id=current_user.id, role=BoardRole.OWNER
        )
    )
    session.add_all(
        [
            BoardColumn(
                board_id=new_board.id, title=name, position=(index + 1) * 1000.0
            )
            for index, name in enumerate(DEFAULT_COLUMNS)
        ]
    )

    await session.commit()
    await session.refresh(new_board)
    return new_board


async def can_view(board: Board, user: User | None, session: AsyncSession) -> bool:
    if board.is_public:
        return True
    if user is None:
        return False

    stmt = select(BoardMember.id).where(
        BoardMember.board_id == board.id,
        BoardMember.user_id == user.id,
    )
    member_id = await session.scalar(stmt)
    return member_id is not None


async def can_edit(board: Board, user: User | None, session: AsyncSession) -> bool:
    if user is None:
        return False

    stmt = select(BoardMember.id).where(
        BoardMember.board_id == board.id,
        BoardMember.user_id == user.id,
    )
    member_id = await session.scalar(stmt)
    return member_id is not None
