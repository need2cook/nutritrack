from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Day, ProductEntity, ExersiceEntity, Diary

from app.modules.base import BaseDAO


class DiaryDAO(BaseDAO):
    model = Diary


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
        from app.modules.products_catalog import ProductDAO

        # 1) Продукт существует?
        product = await ProductDAO.find_one_or_none(session, id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден.",
            )

        # 2) Уже есть запись этого продукта в данном дне?
        existing = await ProductEntityDAO.find_one_or_none(session, day_id=day_id, product_id=product_id)

        if existing:
            # суммируем граммы
            existing.grams = int(existing.grams) + int(grams)
            await session.flush()
            return

        # 3) Создаём новую запись
        try:
            await ProductEntityDAO.add(
                session,
                day_id=day_id,
                product_id=product_id,
                grams=grams,
            )
        except IntegrityError:
            await session.rollback()
            await ProductEntityDAO.update(
                session,
                filter_by={'day_id': day_id, 'product_id': product_id},
                grams=ProductEntity.grams + grams
            )
            await session.flush()


class ProductEntityDAO(BaseDAO):
    model = ProductEntity


class ExersiceEntityDAO(BaseDAO):
    model = ExersiceEntity