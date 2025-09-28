from app.modules.base import Base
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.diaries.models import ExersiceEntity


class Exersice(Base):
    __tablename__ = "exersices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    kcal_30m: Mapped[int] = mapped_column(Integer, nullable=False)

    exersice_entries: Mapped[List["ExersiceEntity"]] = relationship(
        back_populates="exersice",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint("kcal_30m >= 0", name="chk_kcal_non_negative"),
    )