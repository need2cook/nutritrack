from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, UniqueConstraint, Index, CheckConstraint, Date, text
from app.modules.base import Base
import datetime

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.products_catalog.models import Product
    from app.modules.exersices_catalog.models import Exersice


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped["User"] = relationship(back_populates="diary", lazy="selectin")

    days: Mapped[List["Day"]] = relationship(
        back_populates="diary",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Day(Base):
    __tablename__ = "days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    diary_id: Mapped[int] = mapped_column(
        ForeignKey("diaries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    diary: Mapped["Diary"] = relationship(back_populates="days", lazy="selectin")
    user: Mapped["User"] = relationship(back_populates="days", lazy="selectin")

    product_entries: Mapped[List["ProductEntity"]] = relationship(
        back_populates="day",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    exersice_entries: Mapped[List["ExersiceEntity"]] = relationship(
        back_populates="day",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    water_drinked_ml: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))

    __table_args__ = (
        UniqueConstraint("diary_id", "date", name="uq_day_diary_date"),
        Index("ix_days_user_date", "user_id", "date"),
        CheckConstraint("user_id = diary_id", name="chk_day_user_equals_diary"),
        Index("ix_days_diary_date", "diary_id", "date"),
    )



class ProductEntity(Base):
    __tablename__ = "product_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    grams: Mapped[int] = mapped_column(Integer, nullable=False)

    day_id: Mapped[int] = mapped_column(
        ForeignKey("days.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    day: Mapped["Day"] = relationship(back_populates="product_entries", lazy="selectin")
    product: Mapped["Product"] = relationship(back_populates="product_entries", lazy="selectin")

    __table_args__ = (
        CheckConstraint("grams > 0", name="chk_grams_positive"),
        UniqueConstraint("day_id", "product_id", name="uq_day_product"),
    )


class ExersiceEntity(Base):
    __tablename__ = "exersice_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    day_id: Mapped[int] = mapped_column(
        ForeignKey("days.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exersice_id: Mapped[int] = mapped_column(
        ForeignKey("exersices.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    day: Mapped["Day"] = relationship(back_populates="exersice_entries", lazy="selectin")
    exersice: Mapped["Exersice"] = relationship(back_populates="exersice_entries", lazy="selectin")

    __table_args__ = (
        CheckConstraint("minutes > 0", name="chk_minutes_positive"),
        UniqueConstraint("day_id", "exersice_id", name="uq_day_exersice"),
    )
