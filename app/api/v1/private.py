from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User, db_sessions, UserDAO, DayDAO, ProductEntityDAO, ProductDAO
from app.utils.deps import get_current_user_readonly
from datetime import date, datetime
from zoneinfo import ZoneInfo

from .schemas.private import (
    DayOut,
    AddProductOut,
    AddProductIn,
    CreateProductIn,
)


from loguru import logger

router = APIRouter()


@router.get("/day/today", response_model=DayOut)
async def get_today(
    user: User = Depends(get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    tz = "Europe/Moscow"
    today = datetime.now(ZoneInfo(tz)).date()
    day = await DayDAO.find_one_or_none(session, date=today, user_id=user.id)

    if not day:
        await DayDAO.add(
            session,
            diary_id=user.diary.id,
            user_id=user.id,
            date=today,
        )

        day = await DayDAO.find_one_or_none(session, date=today, user_id=user.id)

    return day


@router.get("/day/{target_date}", response_model=DayOut)
async def get_day(
    target_date: date,
    user: User = Depends(get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db_with_commit)
):
    day = await DayDAO.find_one_or_none(session, date=target_date, user_id=user.id)

    if not day:
        await DayDAO.add(
            session,
            diary_id=user.diary.id,
            user_id=user.id,
            date=target_date,
        )

        day = await DayDAO.find_one_or_none(session, date=target_date, user_id=user.id)

    return day


@router.post("/day", response_model=AddProductOut)
async def add_product(
    payload: AddProductIn,
    user: User = Depends(get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    day = await DayDAO.find_one_or_none(session, date=payload.target_date, user_id=user.id)
    if not day:
        await DayDAO.add(
            session,
            diary_id=user.diary.id,
            user_id=user.id,
            date=payload.target_date,
        )
        await session.commit()
        day = await DayDAO.find_one_or_none(session, date=payload.target_date, user_id=user.id)
        if not day:
            raise HTTPException(
                status_code=500, detail="Не удалось создать день.")

    await DayDAO.add_product(
        session,
        day_id=day.id,
        product_id=payload.product_id,
        grams=payload.grams,
    )

    return AddProductOut(success=True)
