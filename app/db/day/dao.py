# app/db/dao/day.py (или где у тебя DayDAO лежит)

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import BaseDAO, Day, Product, ProductEntity


class DayDAO(BaseDAO):
    model = Day

    @staticmethod
    async def add_product(
        session: AsyncSession,
        *,
        day_id: int,
        product_id: int,
        grams: int,
    ) -> None:
        # 1) Продукт существует?
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден.",
            )

        # 2) Уже есть запись этого продукта в данном дне?
        existing = await session.scalar(
            select(ProductEntity)
            .where(
                ProductEntity.day_id == day_id,
                ProductEntity.product_id == product_id,
            )
            .limit(1)
        )

        if existing:
            # суммируем граммы
            existing.grams = int(existing.grams) + int(grams)
            await session.flush()
            return

        # 3) Создаём новую запись
        try:
            session.add(
                ProductEntity(
                    day_id=day_id,
                    product_id=product_id,
                    grams=grams,
                )
            )
            await session.flush()
        except IntegrityError:
            await session.rollback()
            await session.execute(
                update(ProductEntity)
                .where(
                    ProductEntity.day_id == day_id,
                    ProductEntity.product_id == product_id,
                )
                .values(grams=ProductEntity.grams + grams)
            )
            await session.flush()
