# app/modules/diaries/service.py
from __future__ import annotations
from loguru import logger

from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.modules.diaries.dao import DayDAO, ProductEntityDAO, ExersiceEntityDAO

class DiaryService:
    def __init__(self, session: AsyncSession, tz: str = "Europe/Moscow"):
        self.session = session
        self.tz = tz

    def _today(self) -> date:
        return datetime.now(ZoneInfo(self.tz)).date()

    async def get_or_create_day(self, *, user_id: int, diary_id: int, target_date: date) -> object:
        day = await DayDAO.find_one_or_none(self.session, date=target_date, user_id=user_id)
        if day:
            return day

        try:
            await DayDAO.add(
                self.session,
                diary_id=diary_id,
                user_id=user_id,
                date=target_date,
            )
            await self.session.flush()
            day = await DayDAO.find_one_or_none(self.session, date=target_date, user_id=user_id)
            if not day:
                raise HTTPException(status_code=500, detail="Не удалось создать день.")
            return day
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при создании дня (возможно, уже существует).",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при создании дня.") from e

    async def get_today(self, *, user_id: int, diary_id: int):
        target = self._today()
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target)
            await self.session.commit()
            return day
        except HTTPException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось получить текущий день.") from e

    async def get_by_date(self, *, user_id: int, diary_id: int, target_date: date):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            await self.session.commit()
            return day
        except HTTPException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось получить день.") from e

    async def rm_product_from_day(
        self,
        user_id: int, 
        diary_id: int, 
        target_date: date, 
        entry_id: int,
    ):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            deleted = await ProductEntityDAO.delete(self.session, id=entry_id, day_id=day.id)

            if not deleted:
                await self.session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Продукт не был удален.",
                )

            await self.session.commit()
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при удалении продукта из дня.",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при удалении продукта.") from e
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось удалить продукт из дня.") from e
        
    async def rm_exercise_from_day(
        self,
        user_id: int, 
        diary_id: int, 
        target_date: date, 
        entry_id: int,
    ):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            deleted = await ExersiceEntityDAO.delete(self.session, id=entry_id, day_id=day.id)

            if not deleted:
                await self.session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Упражнение не было удалено.",
                )

            await self.session.commit()
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при удалении упражнения из дня.",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при удалении упражнения.") from e
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось удалить упражнение из дня.") from e

    async def add_product_to_day(self, *, user_id: int, diary_id: int, target_date: date, product_id: int, grams: float):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            await DayDAO.add_product(
                self.session,
                day_id=day.id,
                product_id=product_id,
                grams=grams,
            )
            await self.session.commit()
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при добавлении продукта в день.",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при добавлении продукта.") from e
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось добавить продукт в день.") from e
        
    async def add_exercise_to_day(
        self, 
        user_id: int,
        diary_id: int,
        target_date: date, 
        exercise_id: int, 
        minutes: float,
    ):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            await DayDAO.add_exercise(
                self.session,
                day_id=day.id,
                exercise_id=exercise_id,
                minutes=minutes,
            )
            await self.session.commit()
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при добавлении упражнения в день.",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при добавлении упражнения.") from e
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось добавить упражнение в день.") from e
        
    async def add_water_to_day(
        self,
        user_id: int,
        diary_id: int,
        target_date: date, 
        water_mls: int,
    ):
        try:
            day = await self.get_or_create_day(user_id=user_id, diary_id=diary_id, target_date=target_date)
            await DayDAO.add_water(
                session=self.session,
                day_id=day.id,
                water_mls=water_mls
            )

            await self.session.commit()
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфликт при воды в день.",
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка БД при добавлении воды.") from e
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Не удалось добавить воду в день.") from e
        
            