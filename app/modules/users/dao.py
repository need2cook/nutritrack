from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple
from loguru import logger

from .models import User
from app.modules.base import BaseDAO

from app.modules.diaries import DayDAO, DiaryDAO

from datetime import datetime
from zoneinfo import ZoneInfo


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def upsert_user(
        cls,
        session: AsyncSession,
        unique_fields: List[str],
        **values
    ) -> Tuple[User, bool]:
        """Вернёт (user, created)."""
        status = await cls.upsert(session, unique_fields, **values)
        if status == "new":
            logger.warning(f"Новый пользователь: @{values.get('username')} [{values.get('telegram_id')}]")
            user = await cls.find_one_or_none(session, telegram_id=values["telegram_id"])

            # создание дневника
            diary = await DiaryDAO.add(
                session,
                id=user.id
            )


            tz = "Europe/Moscow"
            today = datetime.now(ZoneInfo(tz)).date()

            # создание сегодняшнего дня
            day = await DayDAO.add(
                session,
                diary_id=diary.id,
                user_id=user.id,
                date=today,
            )

            return user, True
        else:
            user = await cls.find_one_or_none(session, telegram_id=values["telegram_id"])
            return user, False
            
