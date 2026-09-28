from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Board(Base):
    __tablename__ = "boards"

    title: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
