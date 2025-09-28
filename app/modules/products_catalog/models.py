from app.modules.base import Base
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.diaries.models import ProductEntity


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

