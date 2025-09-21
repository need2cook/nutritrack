from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import (
    Integer, BigInteger, String, Float, ForeignKey, func,
    Date, Numeric, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


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


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped[User] = relationship(back_populates="diary", lazy="selectin")

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

    date: Mapped[date] = mapped_column(Date, nullable=False)

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

    __table_args__ = (
        UniqueConstraint("diary_id", "date", name="uq_day_diary_date"),
        Index("ix_days_user_date", "user_id", "date"),
        CheckConstraint("user_id = diary_id", name="chk_day_user_equals_diary"),
        Index("ix_days_diary_date", "diary_id", "date"),
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    carbs_100g: Mapped[Numeric] = mapped_column(Numeric(6, 2), nullable=False)
    proteins_100g: Mapped[Numeric] = mapped_column(Numeric(6, 2), nullable=False)
    fats_100g: Mapped[Numeric] = mapped_column(Numeric(6, 2), nullable=False)
    kcal_100g: Mapped[int] = mapped_column(Integer, nullable=False)

    product_entries: Mapped[List["ProductEntity"]] = relationship(
        back_populates="product",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint("carbs_100g >= 0 AND proteins_100g >= 0 AND fats_100g >= 0", name="chk_macros_non_negative"),
        CheckConstraint("kcal_100g >= 0", name="chk_kcal_non_negative"),
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