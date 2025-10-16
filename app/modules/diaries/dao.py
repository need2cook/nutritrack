from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update

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

    @staticmethod
    async def add_exercise(
        session: AsyncSession,
        *,
        day_id: int,
        exercise_id: int,
        minutes: int,
    ) -> None:
        from app.modules.exersices_catalog import ExersiceDAO

        exercise = await ExersiceDAO.find_one_or_none(session, id=exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Упражнение не найдено.",
            )

        existing = await ExersiceEntityDAO.find_one_or_none(session, day_id=day_id, exersice_id=exercise_id)

        if existing:
            # суммируем минуты
            existing.minutes = int(existing.minutes) + int(minutes)
            await session.flush()
            return

        # 3) Создаём новую запись
        try:
            await ExersiceEntityDAO.add(
                session,
                day_id=day_id,
                exersice_id=exercise_id,
                minutes=minutes,
            )
        except IntegrityError:
            await session.rollback()
            await ExersiceEntityDAO.update(
                session,
                filter_by={'day_id': day_id, 'exercise_id': exercise_id},
                minutes=ExersiceEntity.minutes + minutes
            )
            await session.flush()

    @staticmethod
    async def add_water(
        session: AsyncSession,
        *,
        day_id: int,
        water_mls: int,
    ):
        upd = await session.execute(
            sqlalchemy_update(Day)
            .where(Day.id == day_id)
            .values(
                water_drinked_ml=Day.water_drinked_ml + water_mls
            )
        )

        if upd.rowcount != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="День не найден."
            )
        



class ProductEntityDAO(BaseDAO):
    model = ProductEntity


class ExersiceEntityDAO(BaseDAO):
    model = ExersiceEntity