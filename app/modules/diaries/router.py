# app/modules/diaries/router.py
from __future__ import annotations

from fastapi import Body

from datetime import date
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth import AuthService
from app.core.sessionmaker_fastapi import db_sessions
from .schemas import (
    DayOut, 
    AddProductIn, 
    AddProductOut,
    AddExerciseOut,
    AddExerciseIn,
    DeleteProductOut,
    DeleteProductOut,
    DeleteProductIn,
    AddWaterIn,
)
from .service import DiaryService

if TYPE_CHECKING:
    from app.modules.users.models import User
    from .models import Day

router = APIRouter()

@router.get("/day/today", response_model=DayOut)
async def get_today(
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    day: Day = await svc.get_today(user_id=user.id, diary_id=user.diary.id)
    return day

@router.get("/day/{target_date}", response_model=DayOut)
async def get_day(
    target_date: date,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    day = await svc.get_by_date(user_id=user.id, diary_id=user.diary.id, target_date=target_date)
    return day

@router.post("/day/product", response_model=AddProductOut)
async def add_product(
    payload: AddProductIn,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    await svc.add_product_to_day(
        user_id=user.id,
        diary_id=user.diary.id,
        target_date=payload.target_date,
        product_id=payload.product_id,
        grams=payload.grams,
    )
    return AddProductOut(success=True)

@router.delete("/day/{target_date}/product/{entry_id}", response_model=DeleteProductOut)
async def delete_product(
    target_date: date,
    entry_id: int,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    await svc.rm_product_from_day(
        user_id=user.id,
        diary_id=user.diary.id,
        target_date=target_date,
        entry_id=entry_id,
    )
    return DeleteProductOut(success=True)

@router.delete("/day/{target_date}/exercise/{entry_id}", response_model=DeleteProductOut)
async def delete_exercise(
    target_date: date,
    entry_id: int,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    await svc.rm_exercise_from_day(
        user_id=user.id,
        diary_id=user.diary.id,
        target_date=target_date,
        entry_id=entry_id,
    )
    return DeleteProductOut(success=True)


@router.post("/day/exercise", response_model=AddExerciseOut)
async def add_exercise(
    payload: AddExerciseIn,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")
    await svc.add_exercise_to_day(
        user_id=user.id,
        diary_id=user.diary.id,
        target_date=payload.target_date,
        exercise_id=payload.exercise_id,
        minutes=payload.minutes,
    )
    return AddExerciseOut(success=True)
    

@router.put('/day/water', response_model=AddExerciseOut)
async def add_water(
    payload: AddWaterIn,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = DiaryService(session, tz="Europe/Moscow")

    await svc.add_water_to_day(
        user_id=user.id,
        diary_id=user.diary.id,
        target_date=payload.target_date,
        water_mls=payload.water_mls,
    )

    return AddExerciseOut(success=True)

    