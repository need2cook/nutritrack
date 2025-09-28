from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import (
    Integer, BigInteger, String, Float, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.base import Base


if TYPE_CHECKING:
    from app.modules.diaries.models import Diary, Day


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    current_weight: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    diary: Mapped["Diary"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="selectin",
    )

    days: Mapped[List["Day"]] = relationship(
        back_populates="user",
        lazy="selectin",
        viewonly=True,
    )